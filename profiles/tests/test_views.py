from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import UserProfile, SavedRecipe
from recipes.models import Recipe

User = get_user_model()


class ProfileViewsTest(TestCase):
    """Tests for UserProfile views"""

    def setUp(self):
        """Set up a user, profile, and some recipes for testing."""
        self.user = User.objects.create_user(email="testuser@example.com")
        self.client.force_login(self.user)  # Log in the test user
        self.profile = UserProfile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(title="Pasta", ingredients="tomato, basil, garlic")
        self.saved_recipe = SavedRecipe.objects.create(
            user=self.user,
            recipe=self.recipe,
            recipe_name=self.recipe.title,
            ingredients=self.recipe.ingredients,
            instructions="Boil pasta, mix with sauce."
        )

    def test_profile_view_loads(self):
        """Test that the profile page loads correctly."""
        response = self.client.get(reverse("profiles:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Profile")

    def test_update_preferences(self):
        """Test that a user can update their ingredient preferences."""
        response = self.client.post(reverse("profiles:update_preferences"), {"ingredients_to_avoid": "garlic"})
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.ingredients_to_avoid, "garlic")
        self.assertEqual(response.status_code, 302)  # Redirects after saving

    def test_save_recipe(self):
        """Test that a user can save a recipe and it appears on their profile."""
        response = self.client.post(reverse("profiles:save_recipe"), {
            "recipe_name": "New Recipe",
            "ingredients": "flour, sugar, eggs",
            "instructions": "Mix and bake."
        })

        self.assertEqual(response.status_code, 302)  # Redirect after saving
        self.assertTrue(SavedRecipe.objects.filter(user=self.user, recipe__title="New Recipe").exists())

    def test_edit_saved_recipe(self):
        """Test that a user can edit a saved recipe."""
        response = self.client.post(reverse("profiles:edit_saved_recipe", args=[self.saved_recipe.id]), {
            "recipe_name": "Updated Pasta",
            "ingredients": "tomato, basil, olive oil",
            "instructions": "Boil pasta, mix with olive oil."
        })

        self.saved_recipe.refresh_from_db()
        self.assertEqual(self.saved_recipe.recipe_name, "Updated Pasta")
        self.assertEqual(response.status_code, 302)

    def test_delete_saved_recipe(self):
        """Test that a user can delete a saved recipe."""
        response = self.client.post(reverse("profiles:delete_saved_recipe", args=[self.saved_recipe.id]))

        # Ensure it no longer exists
        self.assertFalse(SavedRecipe.objects.filter(id=self.saved_recipe.id).exists())
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
