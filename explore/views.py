from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from profiles.models import UserProfile, SavedRecipe
from recipes.models import Recipe



def explore_page(request):
    """Show saved recipes sorted by popularity and filtered by user preferences."""
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

    # Filter out recipes containing excluded ingredients
    query = Q()
    for ingredient in excluded_ingredients:
        query |= Q(ingredients__icontains=ingredient)  # Case-insensitive match

    if excluded_ingredients:
        saved_recipes = SavedRecipe.objects.exclude(query)
    else:
        saved_recipes = SavedRecipe.objects.all()

    # Count how many times each recipe has been saved
    saved_recipes = saved_recipes.values('recipe_name', 'ingredients', 'instructions').annotate(num_hearts=Count('id')).order_by('-num_hearts')

    return render(request, "explore/explore.html", {"recipes": saved_recipes})




@login_required
def heart_recipe(request, recipe_id):
    """Allow a user to heart (save) a recipe."""
    # Get the saved recipe by ID
    recipe = get_object_or_404(SavedRecipe, id=recipe_id)

    # Check if the user already saved this recipe
    obj, created = SavedRecipe.objects.get_or_create(
        user=request.user,
        recipe_name=recipe.recipe_name,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions
    )

    return JsonResponse({"status": "hearted" if created else "already hearted"})
