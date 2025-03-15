from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from profiles.models import UserProfile, SavedRecipe
from recipes.models import Recipe



def explore_page(request):
    """Show original recipes sorted by popularity and filtered by user preferences."""
    user = request.user

    # Ensure the user is authenticated before querying their profile
    user_profile = None
    if user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass  # Keep user_profile as None

    # Get excluded ingredients (convert comma-separated string to a list)
    excluded_ingredients = (
        [ingredient.strip().lower() for ingredient in user_profile.ingredients_to_avoid.split(",")]
        if user_profile and user_profile.ingredients_to_avoid
        else []
    )

    # Get user's diet preference
    diet_preference = user_profile.diet_preference if user_profile else "none"

    # Define diet-based ingredient exclusions
    diet_exclusions = {
        "vegan": ["chicken", "beef", "pork", "fish", "seafood", "milk", "cheese", "butter", "egg", "honey"],
        "vegetarian": ["chicken", "beef", "pork", "fish", "seafood"],
        "pescatarian": ["chicken", "beef", "pork"],
        "gluten_free": ["wheat", "barley", "rye"],
        "keto": ["sugar", "rice", "bread", "pasta", "potato"]
    }

    # Combine diet exclusions with user’s avoided ingredients
    if diet_preference in diet_exclusions:
        excluded_ingredients.extend(diet_exclusions[diet_preference])

    # Filter out recipes containing excluded ingredients
    query = Q()
    for ingredient in excluded_ingredients:
        query |= Q(ingredients__icontains=ingredient)  # Case-insensitive match

    # Retrieve recipes and apply filters
    recipes = Recipe.objects.all()
    if excluded_ingredients:
        recipes = recipes.exclude(query)

    # Exclude the "Default Recipe" from the explore page
    recipes = recipes.exclude(title="Default Recipe")

    # Ensure recipes are sorted by most hearts (times saved)
    recipes = recipes.annotate(num_hearts=Count('saved_recipes')).order_by('-num_hearts')

    return render(request, "explore/explore.html", {"recipes": recipes})



def heart_recipe(request, recipe_id):
    """Allow a user to heart (save) or un-heart (remove) a recipe from their profile."""
    
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "I'm sorry, you must be logged in to Heart a recipe."},
            status=401,  # HTTP 401 Unauthorized
        )
        
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Prevent saving the default recipe
    if recipe.title == "Default Recipe":
        return JsonResponse({"status": "error", "message": "Default recipe cannot be saved."})

    # Find if the recipe is already saved
    saved_recipe = SavedRecipe.objects.filter(user=request.user, recipe=recipe).first()

    if saved_recipe:
        if saved_recipe in user_profile.hearted_recipes.all():
            # Remove from hearted list
            user_profile.hearted_recipes.remove(saved_recipe)

            # **Now also remove it from the SavedRecipe table for this user**
            saved_recipe.delete()

            return JsonResponse({"status": "removed", "message": "Recipe removed from hearted list and saved recipes."})

        # Otherwise, add to hearted list
        user_profile.hearted_recipes.add(saved_recipe)
        return JsonResponse({"status": "hearted", "message": "Recipe has been hearted."})

    else:
        saved_recipe = SavedRecipe.objects.create(
            user=request.user,
            recipe=recipe,
            recipe_name=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions
        )
        user_profile.hearted_recipes.add(saved_recipe)
        return JsonResponse({"status": "hearted", "message": "Recipe has been hearted."})
