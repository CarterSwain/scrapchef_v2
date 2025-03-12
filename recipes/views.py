import openai
from django.conf import settings
from django.shortcuts import render
from .forms import RecipeInputForm

# Initialize OpenAI client using the new API format
openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

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
            max_tokens=300
        )
        return response.choices[0].message.content.strip()  # Extracting the AI-generated recipe
    except Exception as e:
        return f"Error generating recipe: {str(e)}"

def recipe_view(request):
    """Handles user input and displays generated recipe."""
    recipe = None

    if request.method == "POST":
        form = RecipeInputForm(request.POST)
        if form.is_valid():
            ingredients = [i.strip() for i in form.cleaned_data["ingredients"].split(",")]  # Clean input
            recipe = generate_recipe(ingredients)
    else:
        form = RecipeInputForm()

    return render(request, "recipes/recipe_detail.html", {"form": form, "recipe": recipe})
