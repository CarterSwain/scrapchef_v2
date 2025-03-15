from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create a user with an email (no password required for Google Auth)."""
        if not email:
            raise ValueError("The Email field must be set")  # Prevent empty emails
        email = self.normalize_email(email)  # Normalize email (lowercase)
        extra_fields.setdefault("is_active", True)  # Default: users are active
        user = self.model(email=email, **extra_fields)  # Create a user instance
        user.set_unusable_password()  # Make sure password is not needed
        user.save(using=self._db)  # Save user to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # 🚀 Remove username field entirely
    email = models.EmailField(unique=True)  # Ensure unique email for social auth
    first_name = models.CharField(max_length=30, blank=True, null=True)  # Optional
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"  # Authenticate using email only
    REQUIRED_FIELDS = []  # Remove "username" from required fields

    objects = CustomUserManager()  # Use our custom manager

    def __str__(self):
        return self.email  # Display email instead of username

