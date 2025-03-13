from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from profiles.models import UserProfile, SavedRecipe
from recipes.models import Recipe



def explore_page(request):
    """Show original recipes sorted by popularity and filtered by user preferences."""
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
        recipes = Recipe.objects.exclude(query)
    else:
        recipes = Recipe.objects.all()

    # Count how many times each recipe has been saved
    recipes = recipes.annotate(num_hearts=Count('saved_recipes')).order_by('-num_hearts')

    return render(request, "explore/explore.html", {"recipes": recipes})



@login_required
def heart_recipe(request, recipe_id):
    """Allow a user to heart (save) a recipe to their profile."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Get the Recipe object
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Find an existing saved recipe for this user and recipe (avoid duplicates)
    saved_recipe = SavedRecipe.objects.filter(user=request.user, recipe=recipe).first()

    if not saved_recipe:
        # If no existing saved recipe, create a new one
        saved_recipe = SavedRecipe.objects.create(
            user=request.user,
            recipe=recipe,
            recipe_name=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions
        )

    # Ensure it's added to hearted recipes
    user_profile.hearted_recipes.add(saved_recipe)

    return JsonResponse({"status": "hearted" if created else "already hearted"})