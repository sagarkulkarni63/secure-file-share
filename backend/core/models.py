from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
        ("guest", "Guest"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    mfa_secret = models.CharField(max_length=64, blank=True, null=True)

class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    filename = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to="encrypted/")
    created_at = models.DateTimeField(auto_now_add=True)

class ShareLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="share_links")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    permission = models.CharField(max_length=10, choices=(("view","View"),("download","Download")))
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.expires_at
