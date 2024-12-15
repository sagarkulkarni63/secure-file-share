from rest_framework import views, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.core.files.base import ContentFile
from .models import File, ShareLink
from .serializers import FileSerializer
from .permissions import IsOwnerOrAdmin
from .utils.encryption import encrypt_data, decrypt_data
from .utils.totp import generate_mfa_secret
from .validators import validate_username, validate_password
from .utils.validators import is_safe_filename
from .utils.jwt_tools import generate_access_token
import datetime
from django.http import FileResponse
import jwt

User = get_user_model()

class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = validate_username(request.data.get("username",""))
        password = validate_password(request.data.get("password",""))
        role = request.data.get("role", "user")

        if User.objects.filter(username=username).exists():
            return Response({"error": "User exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, role=role)
        return Response({"message": "Registered successfully"}, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        # if user.mfa_secret:
        #     # Instead of TOTP, we now generate a 4-digit pin.
        #     from core.utils.mfa_temp_store import set_mfa_pin
        #     pin = set_mfa_pin(user.id)
        #     # Inform frontend that MFA is required
        #     return Response({"mfa_required": True, "user_id": user.id, "message": f"MFA code sent. (PIN: {pin} for testing)"},
        #                     status=status.HTTP_200_OK)
        # If no MFA required, set cookie and return token
        access = generate_access_token(user)
        response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=True,    # Adjust based on environment
            samesite='None',  # If cross-site, else omit for same origin dev
            domain=None,
            path="/"
        )
        return response


class MFASetupView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.mfa_secret:
            request.user.mfa_secret = generate_mfa_secret()
            request.user.save()
        return Response({"secret": request.user.mfa_secret}, status=status.HTTP_200_OK)


class MFAConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from core.utils.mfa_temp_store import verify_mfa_pin
        access_token = request.COOKIES.get('access')
        decoded_token = jwt.decode(access_token.encode('utf-8'), settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get("user_id")
        pin = request.data.get("token")
        
        if not user_id or not pin:
            return Response({"error": "User ID and PIN required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate pin
        if verify_mfa_pin(int(user_id), pin):
            # Pin valid: authenticate user fully
            user = get_user_model().objects.get(pk=user_id)
            access = generate_access_token(user)
            response = Response({"message": "MFA confirmed, logged in"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                secure=True,   # Adjust if HTTPS is used
                samesite='None', # if cross-site
                domain=None,
                path="/"
            )
            return response
        else:
            return Response({"error": "Invalid or expired PIN"}, status=status.HTTP_401_UNAUTHORIZED)


ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.png', '.jpg', '.jpeg', '.docx'}  # example

def is_allowed_extension(filename: str):
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        upload_file = request.FILES.get('file')
        if not upload_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not is_allowed_extension(upload_file.name):
            return Response({"error": "Invalid file type."}, status=status.HTTP_400_BAD_REQUEST)

        data = upload_file.read()
        enc_data = encrypt_data(data)
        new_file = File(owner=request.user, filename=upload_file.name)
        new_file.encrypted_file.save(upload_file.name, ContentFile(enc_data))
        return Response(FileSerializer(new_file).data, status=status.HTTP_201_CREATED)


class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return File.objects.all()
        return File.objects.filter(owner=user)


class FileDownloadView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, *args, **kwargs):
        try:
            file_obj = self.get_object()
            with file_obj.encrypted_file.open('rb') as f:
                enc_data = f.read()
            
            try:
                dec_data = decrypt_data(enc_data)
            except Exception as decrypt_error:
                # Log the specific decryption error
                return Response(
                    {"error": "File decryption failed"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Determine content type based on file extension
            content_type = mimetypes.guess_type(file_obj.filename)[0] or 'application/octet-stream'

            file_stream = BytesIO(dec_data)
            response = FileResponse(
                file_stream, 
                as_attachment=True, 
                filename=file_obj.filename,
                content_type=content_type
            )
            return response

        except File.DoesNotExist:
            return Response(
                {"error": "File not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Log unexpected errors
            print(e)
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ShareFileView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_id = request.data.get("file_id")
        permission = request.data.get("permission", "view")
        validity_hours = int(request.data.get("validity", 1))
        try:
            file_obj = File.objects.get(pk=file_id, owner=request.user)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        expires_at = timezone.now() + datetime.timedelta(hours=validity_hours)
        link = ShareLink.objects.create(file=file_obj, expires_at=expires_at, permission=permission)
        share_url = f"http://localhost:8000/api/share/{link.token}/"
        return Response({"share_url": share_url, "expires_at": expires_at}, status=status.HTTP_201_CREATED)

class AccessShareView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            link = ShareLink.objects.get(token=token)
        except ShareLink.DoesNotExist:
            return Response({"error": "Invalid link"}, status=status.HTTP_404_NOT_FOUND)

        if not link.is_valid():
            return Response({"error": "Link expired"}, status=status.HTTP_410_GONE)

        # If not logged in, treat as guest (just view if allowed)
        user = request.user if request.user.is_authenticated else None
        if link.permission == "view":
            # Return file metadata only
            return Response({"file_id": link.file.id, "filename": link.file.filename, "permission": "view"}, status=status.HTTP_200_OK)
        elif link.permission == "download":
            # Check if logged in or Admin/Owner or allowed by link?
            # For simplicity, link alone grants permission
            with link.file.encrypted_file.open('rb') as f:
                enc_data = f.read()
            dec_data = decrypt_data(enc_data)
            response = Response(dec_data, content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{link.file.filename}"'
            return response

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        return response
