from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from recipes.models import Recipe
from profiles.models import UserProfile

User = get_user_model()

class RecipeViewTest(TestCase):
    """Tests for the recipe generation view."""

    def setUp(self):
        """Set up a user and user profile for testing."""
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_recipe_view_loads(self):
        """Ensure the recipe page loads correctly for logged-in users."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("generate_recipe"))  # Adjust URL name if needed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter Ingredients")

    def test_recipe_view_redirects_anonymous_users(self):
        """Ensure anonymous users are redirected to login."""
        response = self.client.get(reverse("generate_recipe"))
        self.assertEqual(response.status_code, 302)  # Redirect expected

    def test_invalid_ingredient_input(self):
        """Ensure invalid ingredient input returns an error."""
        self.client.force_login(self.user)
        response = self.client.post(reverse("generate_recipe"), {"ingredients": "!!!, 123, @#$%"})
        self.assertContains(response, "Invalid ingredient", status_code=200)

    @patch("recipes.views.openai_client.chat.completions.create")
    def test_recipe_generation(self, mock_openai):
        """Mock OpenAI API to test recipe generation."""
        self.client.force_login(self.user)

        mock_openai.return_value.choices = [
            type("Choice", (object,), {"message": type("Message", (object,), {"content": "Title: AI Recipe\n\nIngredients:\nIngredient 1, Ingredient 2\n\nInstructions:\nStep 1, Step 2"})})
        ]

        response = self.client.post(reverse("generate_recipe"), {"ingredients": "chicken, rice, garlic"})
        self.assertContains(response, "AI Recipe")
