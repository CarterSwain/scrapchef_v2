from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import SavedRecipe


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
def profile_view(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).order_by('-updated_at')

    # Debugging print
    print("Saved Recipes for User:", request.user, saved_recipes)

    paginator = Paginator(saved_recipes, 5)  # Show 5 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profiles/profile.html', {'page_obj': page_obj})
