from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import File
from io import BytesIO

User = get_user_model()

class ShareTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("sharer", "pass12345")

        # login user
        self.user.mfa_secret = None
        self.user.save()
        login_resp = self.client.post("/api/login/", {"username":"sharer","password":"pass12345"})
        self.client.cookies["access"] = login_resp.cookies.get("access")

        # Upload a file
        fcontent = BytesIO(b"secret data")
        fcontent.name = "secret.txt"
        upload_resp = self.client.post("/api/files/upload/", {"file": fcontent}, format="multipart")
        self.assertEqual(upload_resp.status_code, 201)
        self.file_id = upload_resp.data["id"]

    def test_share_file(self):
        resp = self.client.post("/api/share/", {"file_id": self.file_id, "validity":1, "permission":"view"}, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("share_url", resp.data)
