from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import IngredientPreferencesForm
from .models import SavedRecipe, UserProfile


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
    if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")

        print("Saving Recipe:", recipe_name, ingredients, instructions)  # Debugging print

        if recipe_name and ingredients and instructions:
            saved_recipe = SavedRecipe.objects.create(
                user=request.user,
                recipe_name=recipe_name,
                ingredients=ingredients,
                instructions=instructions
            )
            print("Recipe Saved Successfully:", saved_recipe)  # Debugging print

            return redirect('profiles:profile')  # Redirect to profile after saving

    return redirect('home')


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
    saved_recipes = SavedRecipe.objects.filter(user=request.user).order_by('-updated_at')

    # Debugging print
    print("Saved Recipes for User:", request.user, saved_recipes)

    paginator = Paginator(saved_recipes, 5)  # Show 5 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profiles/profile.html', {'page_obj': page_obj})
