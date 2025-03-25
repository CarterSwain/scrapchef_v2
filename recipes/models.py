from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

