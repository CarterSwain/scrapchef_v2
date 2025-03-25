from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from recipes.models import Recipe 

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ingredient Preferences
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
    
    # Track Hearted Recipes
    hearted_recipes = models.ManyToManyField('SavedRecipe', related_name="hearted_by_users", blank=True)

    def __str__(self):
        return self.user.email


class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saved_recipes")  
    recipe_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    uploaded_image = models.ImageField(
        upload_to='user_uploaded_recipes/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    use_uploaded_image = models.BooleanField(default=False)  # Checkbox toggle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.recipe.title} saved by {self.user.email}"