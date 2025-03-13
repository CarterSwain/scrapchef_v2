from django.db import models
from django.conf import settings  
from recipes.models import Recipe  # Import existing Recipe model

class UserSavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"
