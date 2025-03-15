from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class GoogleAuthTest(TestCase):
    def test_google_login_redirect(self):
        """Check if Google login page includes OAuth button."""
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)  # Expect 200 since login page loads
        self.assertContains(response, "Sign in with Google")  # Check for Google OAuth button

    def test_user_can_logout(self):
        """Ensure user can log out successfully."""
        user = User.objects.create_user(email="testuser@example.com")  # 🔥 Removed username=None
        self.client.force_login(user)
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)  # Expect redirect to homepage

    def test_auth_persists_across_sessions(self):
        """Ensure authentication persists after session reload."""
        user = User.objects.create_user(email="persistuser@example.com")  # 🔥 Removed username=None
        self.client.force_login(user)

        # Simulate session reload
        session = self.client.session
        session.save()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

