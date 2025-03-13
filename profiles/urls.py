from django.urls import path
from .views import profile_view, edit_saved_recipe, save_recipe, delete_saved_recipe, update_preferences

app_name = "profiles"

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path("preferences/", update_preferences, name="update_preferences"),
    path('recipe/edit/<int:recipe_id>/', edit_saved_recipe, name='edit_saved_recipe'),
    path('recipe/delete/<int:recipe_id>/', delete_saved_recipe, name='delete_saved_recipe'),
    path('save/', save_recipe, name='save_recipe'),  # Route for saving recipes
]
