from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from profiles.models import UserProfile, SavedRecipe  

User = get_user_model()

class ExploreViewsTest(TestCase):
    """ General Explore page tests """
    def setUp(self):
        """Set up a user, profile, and some recipes for testing."""
        self.user = User.objects.create_user(email="testuser@example.com")
        self.profile = UserProfile.objects.create(user=self.user, diet_preference="vegan")

        # Create some recipes
        self.recipe1 = Recipe.objects.create(title="Vegan Salad", ingredients="lettuce, tomato, cucumber")
        self.recipe2 = Recipe.objects.create(title="Chicken Soup", ingredients="chicken, broth, carrot")

    def test_explore_page_loads(self):
        """Test that the explore page loads correctly."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("explore"))
        self.assertEqual(response.status_code, 200, "Explore page did not load properly.")
        self.assertContains(response, "Explore Recipes")

    def test_explore_page_filters_recipes_based_on_preferences(self):
        """Test that the explore page filters out recipes based on user diet."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("explore"))

        self.assertContains(response, "Vegan Salad", msg_prefix="Vegan recipe should be visible.")
        self.assertNotContains(response, "Chicken Soup", msg_prefix="Non-vegan recipe should be filtered out.")



class HeartRecipeTest(TestCase):
    """ Tests for hearting/unhearting recipes stored in SavedRecipe """
    def setUp(self):
        """Set up a user, profile, and some recipes for hearting tests."""
        self.user = User.objects.create_user(email="heartuser@example.com")
        self.profile = UserProfile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(title="Pasta", ingredients="tomato, basil, garlic")
        self.url = reverse("heart_recipe", args=[self.recipe.id])

    def test_authenticated_user_can_heart_recipe(self):
        """Ensure a logged-in user can heart a recipe."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200, "Hearting a recipe should return a 200 status.")
        self.assertTrue(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists(), "Recipe should be saved.")

        saved_recipe = SavedRecipe.objects.get(user=self.user, recipe=self.recipe)
        self.assertIn(saved_recipe, self.profile.hearted_recipes.all(), "Recipe should be in profile's hearted list.")

    def test_authenticated_user_cannot_heart_recipe_twice(self):
        """Ensure a logged-in user cannot heart the same recipe twice."""
        self.client.force_login(self.user)

        # First hearting should be successful
        self.client.post(self.url)

        # Second hearting should **not** create a duplicate
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200, "Second heart attempt should not fail.")
        self.assertEqual(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).count(), 1, "User should only have one saved instance of a recipe.")

    def test_authenticated_user_can_unheart_recipe(self):
        """Ensure a logged-in user can remove a hearted recipe."""
        self.client.force_login(self.user)
        saved_recipe = SavedRecipe.objects.create(user=self.user, recipe=self.recipe)

        self.profile.hearted_recipes.add(saved_recipe)
        self.assertTrue(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists(), "Recipe should be saved before unhearting.")

        response = self.client.post(self.url)

        # Correct Assertion: Only remove from profile hearted list
        self.assertNotIn(saved_recipe, self.profile.hearted_recipes.all(), "Recipe should be removed from user's profile hearted list.")

        # Ensure the `SavedRecipe` record still exists
        self.assertTrue(SavedRecipe.objects.filter(user=self.user, recipe=self.recipe).exists(), "SavedRecipe record should still exist.")

    def test_unauthenticated_user_cannot_heart_recipe(self):
        """Ensure unauthenticated users cannot heart a recipe."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302, "Unauthenticated users should be redirected to login.")
        self.assertEqual(SavedRecipe.objects.filter(recipe=self.recipe).count(), 0, "No recipes should be saved.")
