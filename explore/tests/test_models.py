from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from recipes.models import Recipe
from profiles.models import SavedRecipe, UserProfile  

User = get_user_model()

class SavedRecipeModelTest(TestCase):
    """Test the SavedRecipe model and its integration with UserProfile."""

    def setUp(self):
        """Set up a user, profile, and a recipe."""
        self.user = User.objects.create_user(email="test@example.com")
        self.profile = UserProfile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(title="Spaghetti", ingredients="noodles, tomato sauce")

    def test_create_saved_recipe(self):
        """Test that a user can save a recipe and it is linked correctly."""
        saved_recipe = SavedRecipe.objects.create(user=self.user, recipe=self.recipe)

        self.assertEqual(saved_recipe.user, self.user, "Saved recipe user mismatch.")
        self.assertEqual(saved_recipe.recipe, self.recipe, "Saved recipe mismatch.")
        self.assertEqual(str(saved_recipe), f"{self.recipe.title} saved by {self.user.email}")

    def test_saved_recipe_appears_in_user_profile(self):
        """Test that hearted recipes are correctly stored in UserProfile."""
        saved_recipe = SavedRecipe.objects.create(user=self.user, recipe=self.recipe)
        self.profile.hearted_recipes.add(saved_recipe)

        self.assertIn(saved_recipe, self.profile.hearted_recipes.all(), "Recipe should be in user's hearted list.")

    def test_saved_recipe_prevents_duplicates(self):
        """Ensure a user cannot save the same recipe multiple times."""
        SavedRecipe.objects.create(user=self.user, recipe=self.recipe)

        with self.assertRaises(IntegrityError, msg="Expected IntegrityError for duplicate save."):
            SavedRecipe.objects.create(user=self.user, recipe=self.recipe)

    def test_deleting_saved_recipe_removes_it_from_profile(self):
        """Test that deleting a saved recipe also removes it from the profile's hearted list."""
        saved_recipe = SavedRecipe.objects.create(user=self.user, recipe=self.recipe)
        self.profile.hearted_recipes.add(saved_recipe)

        # Ensure it's saved before deleting
        self.assertIn(saved_recipe, self.profile.hearted_recipes.all(), "Recipe should be in profile before deletion.")

        # Delete the saved recipe
        saved_recipe.delete()

        # Check that it was removed from both the database and the profile
        self.assertFalse(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists(), "Recipe should be deleted from DB.")
        self.assertNotIn(saved_recipe, self.profile.hearted_recipes.all(), "Recipe should be removed from profile's hearted list.")
