from django.urls import path
from .views import recipe_view

urlpatterns = [
    path("generate/", recipe_view, name="generate_recipe"),
]
