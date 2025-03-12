from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class NoPasswordAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True  # Allow signups, but only through Google

    def authenticate(self, request, **credentials):
        raise PermissionDenied("Password authentication is disabled. Please use Google login.")

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Automatically log in existing users or create a new one without extra signup steps.
        """
        user_email = sociallogin.user.email

        if not user_email:
            raise PermissionDenied("Email is required for authentication.")

        try:
            # Check if user already exists in the database
            existing_user = User.objects.get(email=user_email)
            sociallogin.connect(request, existing_user)  # Auto-link social account
        except User.DoesNotExist:
            # Auto-create a user if they don't exist and log them in
            sociallogin.user.is_active = True
            sociallogin.user.save()
        
        return redirect("/profile/")  # Redirect to profile after successful login
