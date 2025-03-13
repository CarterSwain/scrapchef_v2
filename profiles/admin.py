from django.contrib import admin
from .models import UserProfile, SavedRecipe

admin.site.register(UserProfile)
admin.site.register(SavedRecipe)
