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

    # ✅ Ensure recipes are sorted by most hearts (times saved)
    recipes = recipes.annotate(num_hearts=Count('saved_recipes')).order_by('-num_hearts')

    return render(request, "explore/explore.html", {"recipes": recipes})





@login_required
def heart_recipe(request, recipe_id):
    """Allow a user to heart (save) or un-heart (remove) a recipe from their profile."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Get the Recipe object
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Check if this is the "default recipe" (adjust title accordingly)
    if recipe.title == "Default Recipe":
        return JsonResponse({"status": "error", "message": "Default recipe cannot be saved."})

    # Find if this recipe is already saved by the user
    saved_recipe = SavedRecipe.objects.filter(user=request.user, recipe=recipe).first()

    if saved_recipe:
        if saved_recipe in user_profile.hearted_recipes.all():
            # Remove from 'hearted' list
            user_profile.hearted_recipes.remove(saved_recipe)
            
            # Delete the saved recipe from profile
            saved_recipe.delete()
            
            return JsonResponse({"status": "removed", "message": "You have removed this recipe from your saved recipes."})
        
        # If it was not 'hearted' before, 'heart' it
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