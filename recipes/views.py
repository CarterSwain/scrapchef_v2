import openai
import re
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .forms import RecipeInputForm

# Initialize OpenAI client using the new API format
openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def validate_ingredients(ingredients):
    """Validates the ingredient list before sending it to OpenAI API."""
    
    # Check if input is empty
    if not ingredients or all(i.strip() == "" for i in ingredients):
        return "Ingredient list cannot be empty."

    # Ensure each ingredient only contains letters, spaces, and hyphens
    for ingredient in ingredients:
        if not re.match(r"^[a-zA-Z\s\-]+$", ingredient.strip()):
            return f"Invalid ingredient: {ingredient}. Ingredients should only contain letters and spaces."

    # Limit ingredient count (to avoid overly long prompts)
    if len(ingredients) > 15:
        return "Too many ingredients. Please enter up to 15 ingredients."

    # Limit ingredient length per word (to prevent extremely long words)
    if any(len(ingredient.strip()) > 30 for ingredient in ingredients):
        return "Ingredient names should be at most 30 characters long."

    return None  # No validation errors

def generate_recipe(ingredients):
    """Call OpenAI to generate a recipe using only the given ingredients."""
    ingredients_list = ", ".join(ingredients)
    
    prompt = (
        f"Create a simple, delicious recipe using ONLY the following ingredients: {ingredients_list}. "
        "Do not add any extra ingredients. Provide a short title, a list of steps, and clear instructions."
    )
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef who strictly follows ingredient limitations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()  # Extracting the AI-generated recipe
    except Exception as e:
        return f"Error generating recipe: {str(e)}"

@login_required  # Restrict this view to logged-in users
def recipe_view(request):
    """Handles user input and displays generated recipe."""
    recipe = None
    error_message = None  # Store validation errors

    if request.method == "POST":
        form = RecipeInputForm(request.POST)
        if form.is_valid():
            ingredients = [i.strip() for i in form.cleaned_data["ingredients"].split(",") if i.strip()]  # Clean input
            
            # Validate ingredients before calling OpenAI
            validation_error = validate_ingredients(ingredients)
            if validation_error:
                error_message = validation_error  # Store error message for template
            else:
                recipe = generate_recipe(ingredients)  # Generate recipe if input is valid

    else:
        form = RecipeInputForm()

    return render(request, "recipes/recipe_detail.html", {"form": form, "recipe": recipe, "error_message": error_message})

