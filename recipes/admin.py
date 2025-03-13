from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Display these fields in the admin list view
    search_fields = ('title', 'ingredients')  # Allow searching by title and ingredients
    list_filter = ('created_at',)  # Filter recipes by creation date
    ordering = ('-created_at',)  # Order by most recent recipes


