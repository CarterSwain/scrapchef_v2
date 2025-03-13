from django.urls import path
from .views import explore_page, heart_recipe

urlpatterns = [
    path("", explore_page, name="explore"),
    path("heart/<int:recipe_id>/", heart_recipe, name="heart_recipe"),
]
