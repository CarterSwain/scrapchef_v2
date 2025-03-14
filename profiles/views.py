from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import IngredientPreferencesForm
from .models import SavedRecipe, UserProfile
from recipes.models import Recipe


@login_required
def update_preferences(request):
    """Allow users to update their ingredient preferences and diet choices."""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = IngredientPreferencesForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile")  # Redirect to profile after saving
    else:
        form = IngredientPreferencesForm(instance=user_profile)

    return render(request, "profiles/preferences.html", {"form": form})



@login_required
def save_recipe(request):
    """Allow a user to save a new recipe and redirect to profile page."""
    if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")

        # Find or create the corresponding Recipe
        recipe, created = Recipe.objects.get_or_create(
            title=recipe_name,
            defaults={
                "ingredients": ingredients,
                "instructions": instructions
            }
        )

        # Create a new SavedRecipe linked to the Recipe
        saved_recipe = SavedRecipe.objects.create(
            user=request.user,
            recipe=recipe,
            recipe_name=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions
        )

        return redirect("profiles:profile")  # Redirect to the user's profile page

    return redirect("home")  # Redirect to home if accessed incorrectly



@login_required
def edit_saved_recipe(request, recipe_id):
    recipe = get_object_or_404(SavedRecipe, id=recipe_id, user=request.user)
    
    if request.method == "POST":
        recipe.recipe_name = request.POST['recipe_name']
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']
        recipe.save()
        return redirect('profiles:profile')  # Redirect back to the profile page

    return render(request, 'profiles/edit_recipe.html', {'recipe': recipe})


@login_required
def delete_saved_recipe(request, recipe_id):
    """Delete a saved recipe only if it belongs to the logged-in user."""
    recipe = get_object_or_404(SavedRecipe, id=recipe_id, user=request.user)
    
    if request.method == "POST":  # Ensure it's a POST request
        recipe.delete()
        return redirect('profiles:profile')  # Redirect to profile after deletion

    return render(request, 'profiles/confirm_delete.html', {'recipe': recipe})


@login_required
def profile_view(request):
    """Display user profile with all saved (including hearted) recipes."""
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Combine saved and hearted recipes without duplicates
    saved_recipes = SavedRecipe.objects.filter(user=request.user)
    hearted_recipes = user_profile.hearted_recipes.all()

    all_saved_recipes = (saved_recipes | hearted_recipes).distinct()  # Remove duplicates

    # Pagination setup
    paginator = Paginator(all_saved_recipes, 5)  # Show 5 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "profiles/profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,  # Includes both saved and hearted recipes
    })
