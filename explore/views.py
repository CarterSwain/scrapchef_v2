from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from profiles.models import UserProfile
from recipes.models import Recipe
from .models import UserSavedRecipe


def explore_page(request):
    """Show recipes sorted by hearts and filtered by user preferences."""
    user = request.user

    # Try to get the user's profile
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    # Get excluded ingredients (convert comma-separated string to a list)
    excluded_ingredients = (
        [ingredient.strip().lower() for ingredient in user_profile.ingredients_to_avoid.split(",")]
        if user_profile and user_profile.ingredients_to_avoid
        else []
    )

    # Filter recipes to exclude those containing any unwanted ingredients
    query = Q()
    for ingredient in excluded_ingredients:
        query |= Q(ingredients__icontains=ingredient)  # Case-insensitive match

    if excluded_ingredients:
        recipes = Recipe.objects.exclude(query)
    else:
        recipes = Recipe.objects.all()

    # Order by number of hearts
    recipes = recipes.annotate(num_hearts=Count('usersavedrecipe')).order_by('-num_hearts')

    return render(request, "explore/explore.html", {"recipes": recipes})



@login_required
def heart_recipe(request, recipe_id):
    """Allow a user to heart (save) a recipe."""
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Check if user already hearted it
    obj, created = UserSavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)

    return JsonResponse({"status": "hearted" if created else "already hearted"})
