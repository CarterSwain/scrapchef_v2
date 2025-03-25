from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
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
        image_url = request.POST.get("image_url")
        

        # Find or create the corresponding Recipe
        recipe, created = Recipe.objects.get_or_create(
            title=recipe_name,
            defaults={
                "ingredients": ingredients,
                "instructions": instructions,
                "image_url": image_url
            }
        )
        
        # If the recipe already exists but image_url is missing, update it
        if not recipe.image_url and image_url:
            recipe.image_url = image_url
            recipe.save()

        # Create a new SavedRecipe linked to the Recipe
        saved_recipe = SavedRecipe.objects.create(
            user=request.user,
            recipe=recipe,
            recipe_name=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            image_url=recipe.image_url
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

        # Handle optional user image
        if 'uploaded_image' in request.FILES:
            # If a new image was uploaded, delete the old one
            if recipe.uploaded_image and default_storage.exists(recipe.uploaded_image.name):
                default_storage.delete(recipe.uploaded_image.name)

            recipe.uploaded_image = request.FILES['uploaded_image']
            recipe.use_uploaded_image = True  # default to using the uploaded one if provided

        elif 'remove_uploaded_image' in request.POST:
            if recipe.uploaded_image and default_storage.exists(recipe.uploaded_image.name):
                default_storage.delete(recipe.uploaded_image.name)
            recipe.uploaded_image = None
            recipe.use_uploaded_image = False

        else:
            # Checkbox for using uploaded image
            recipe.use_uploaded_image = request.POST.get('use_uploaded_image') == 'on'

        recipe.save()
        return redirect('profiles:profile')

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
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Combine saved and hearted recipes without duplicates
    saved_recipes = SavedRecipe.objects.filter(user=request.user)
    hearted_recipes = user_profile.hearted_recipes.all()

    all_saved_recipes = (saved_recipes | hearted_recipes).distinct().order_by('-created_at') 

    # Pagination setup
    paginator = Paginator(all_saved_recipes, 5)  # Show 5 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "profiles/profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,  # Includes both saved and hearted recipes
    })

