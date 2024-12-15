from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_register(self):
        response = self.client.post("/api/register/", {"username":"newuser","password":"strongpass"})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.post("/api/login/", {"username":self.username,"password":self.password})
        self.assertEqual(response.status_code, 200)
        self.assertIn("mfa_required", response.data)
