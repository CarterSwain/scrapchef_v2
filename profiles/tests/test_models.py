from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from profiles.models import UserProfile, SavedRecipe

User = get_user_model()


class UserProfileModelTest(TestCase):
    """Tests for the UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_creation(self):
        """Test that a UserProfile is correctly linked to a user."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(str(self.profile), self.user.email) 



class SavedRecipeModelTest(TestCase):
    """Tests for the SavedRecipe model"""

    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com")
        self.recipe = Recipe.objects.create(title="Pasta", ingredients="tomato, basil, garlic")

    def test_create_saved_recipe(self):
        """Test that a user can save a recipe and it is linked correctly."""
        saved_recipe = SavedRecipe.objects.create(
            user=self.user,
            recipe=self.recipe,
            recipe_name=self.recipe.title,
            ingredients=self.recipe.ingredients,
            instructions="Boil pasta, mix with sauce."
        )

        self.assertEqual(saved_recipe.user, self.user)
        self.assertEqual(saved_recipe.recipe, self.recipe)
        self.assertEqual(str(saved_recipe), f"{self.recipe.title} saved by {self.user.email}")

    def test_saved_recipe_prevents_duplicates(self):
        """Ensure a user cannot save the same recipe multiple times."""
        SavedRecipe.objects.create(user=self.user, recipe=self.recipe, recipe_name=self.recipe.title, ingredients=self.recipe.ingredients, instructions="Boil pasta.")

        with self.assertRaises(Exception):  # Should fail due to unique constraint
            SavedRecipe.objects.create(user=self.user, recipe=self.recipe, recipe_name=self.recipe.title, ingredients=self.recipe.ingredients, instructions="Boil pasta.")
