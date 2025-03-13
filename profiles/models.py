from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
      # New fields for ingredient preferences
    ingredients_to_avoid = models.TextField(blank=True, null=True, help_text="Comma-separated list of ingredients to avoid.")
    diet_preference = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ("vegan", "Vegan"),
            ("vegetarian", "Vegetarian"),
            ("pescatarian", "Pescatarian"),
            ("gluten_free", "Gluten-Free"),
            ("keto", "Keto"),
            ("none", "No Preference"),
        ],
        default="none"
    )

    def __str__(self):
        return self.user.username


class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.recipe_name} saved by {self.user.username}"
