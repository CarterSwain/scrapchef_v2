from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class AdminUserTest(TestCase):
    def test_create_user_in_admin(self):
        """Ensure superuser can create a new user via admin."""
        user = User.objects.create_user(email="testuser@example.com")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_active)
