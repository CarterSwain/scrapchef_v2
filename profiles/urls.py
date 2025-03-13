from django.urls import path
from .views import profile_view, edit_saved_recipe, save_recipe

app_name = "profiles"

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('recipe/edit/<int:recipe_id>/', edit_saved_recipe, name='edit_saved_recipe'),
    path('save/', save_recipe, name='save_recipe'),  # Route for saving recipes
]
