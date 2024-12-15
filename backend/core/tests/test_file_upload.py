from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from io import BytesIO

User = get_user_model()

class FileUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("uploader", "pass12345")
        # Login and get token
        login_resp = self.client.post("/api/login/", {"username":"uploader","password":"pass12345"})
        # MFA not set up, so no token yet. Let's disable MFA for simplicity in testing:
        self.user.mfa_secret = None
        self.user.save()
        login_resp = self.client.post("/api/login/", {"username":"uploader","password":"pass12345"})
        self.assertEqual(login_resp.status_code, 200)
        # Extract cookie from response
        # For testing in DRF, we can just store cookie manually:
        self.client.cookies["access"] = login_resp.cookies.get("access")

    def test_upload_file(self):
        file_content = BytesIO(b"test file content")
        file_content.name = "testfile.txt"
        response = self.client.post("/api/files/upload/", {"file": file_content}, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertIn("filename", response.data)
