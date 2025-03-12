from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure unique email for social auth
    first_name = models.CharField(max_length=30, blank=True, null=True)  # Add first name
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"  # Make email the primary identifier
    REQUIRED_FIELDS = ["username"]  # Keep username but require it

    def __str__(self):
        return self.email  # Display email instead of username
