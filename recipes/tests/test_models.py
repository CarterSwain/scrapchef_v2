from django.test import TestCase
from recipes.models import Recipe

class RecipeModelTest(TestCase):
    """Tests for the Recipe model."""

    def setUp(self):
        """Set up a recipe instance for testing."""
        self.recipe = Recipe.objects.create(
            title="Spaghetti Carbonara",
            ingredients="Pasta, eggs, pancetta, parmesan, black pepper",
            instructions="Cook pasta. Fry pancetta. Mix eggs and cheese. Combine everything."
        )

    def test_recipe_creation(self):
        """Ensure recipes are created correctly."""
        self.assertEqual(self.recipe.title, "Spaghetti Carbonara")
        self.assertIn("Pasta", self.recipe.ingredients)
        self.assertTrue(self.recipe.instructions.startswith("Cook pasta"))

    def test_recipe_str(self):
        """Test the string representation of a recipe."""
        self.assertEqual(str(self.recipe), "Spaghetti Carbonara")
