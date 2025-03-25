import openai
import re
import logging
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .forms import RecipeInputForm
from profiles.models import UserProfile

# Initialize OpenAI client using the new API format
openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Set up logging for tracking API errors
logger = logging.getLogger(__name__)


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




def generate_recipe(ingredients, user):
    """Generate a structured recipe using only the given ingredients, while considering user preferences."""
    
    # Retrieve user preferences
    user_profile = UserProfile.objects.filter(user=user).first()
    
    # Get ingredients to avoid
    avoided_ingredients = user_profile.ingredients_to_avoid.split(",") if user_profile and user_profile.ingredients_to_avoid else []
    avoided_ingredients = [i.strip().lower() for i in avoided_ingredients if i.strip()]
    
    # Filter out avoided ingredients
    filtered_ingredients = [i for i in ingredients if i.lower() not in avoided_ingredients]
    
    # If all ingredients are avoided, return an error
    if not filtered_ingredients:
        return None, "Error: All entered ingredients are in your 'Avoid' list. Please adjust your preferences."

    # Get the diet preference
    diet_preference = user_profile.diet_preference if user_profile and user_profile.diet_preference and user_profile.diet_preference != "none" else None

    # Create prompt with filtered ingredients and diet preference
    ingredients_list = ", ".join(filtered_ingredients)
    
    prompt = (
        f"Create a simple, delicious recipe using ONLY the following ingredients: {ingredients_list}. "
        "Provide a short, creative recipe title, a list of ingredients, and clear step-by-step instructions. "
        "Format your response as:\n\nTitle: <title>\n\nIngredients:\n<list>\n\nInstructions:\n<steps>"
    )
    
    if diet_preference:
        prompt += f" Ensure the recipe follows a {diet_preference} diet."

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a professional chef who strictly follows ingredient limitations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Check if response is empty or incomplete
        if not response or not response.choices:
            logger.error("OpenAI API returned an empty response.")
            return None, "Error: The AI could not generate a recipe at this time. Please try again."

        raw_recipe = response.choices[0].message.content.strip()

        # Use regex to extract structured data (Title, Ingredients, Instructions)
        match = re.search(r'Title:\s*(?P<title>.*?)\n\nIngredients:\s*(?P<ingredients>.*?)\n\nInstructions:\s*(?P<instructions>.*)', raw_recipe, re.DOTALL)

        if match:
            recipe_data = {
                "title": match.group("title").strip(),
                "ingredients": "Ingredients:\n" + match.group("ingredients").strip(),
                "instructions": "Instructions:\n" + match.group("instructions").strip(),
            }
        else:
            # If regex fails, use fallback method
            recipe_data = {
                "title": f"Recipe with {ingredients_list}",  # Unique fallback title
                "ingredients": "Ingredients:\n" + ingredients_list,
                "instructions": raw_recipe  # Save full response as instructions
            }

        # DALL·E Image Generation (now runs regardless of regex outcome)
        try:
            image_prompt = (
                f"A realistic overhead photo of a plated dish called '{recipe_data['title']}', made strictly with only the following ingredients: {ingredients_list}. "
                "Do NOT include any ingredients or garnishes not listed. Do NOT include any text, labels, writing, or characters in the image.. No background props or items outside the dish. The food should look vibrant, appetizing, and clearly reflect ONLY the given ingredients in list."
            )

            image_response = openai_client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            recipe_data["image_url"] = image_response.data[0].url
        except Exception as e:
            logger.error(f"DALL·E image generation failed: {e}")
            recipe_data["image_url"] = None

        return recipe_data, None  # Return structured data and no error

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return None, "Error: There was a problem communicating with the AI. Please try again later."

    except openai.OpenAIError as e:
        logger.error(f"Unexpected OpenAI error: {e}")
        return None, "Error: An unexpected issue occurred while generating the recipe."

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return None, "Error: Something went wrong. Please try again."



@login_required
def recipe_view(request):
    """Handles user input and displays generated recipe with error handling."""
    recipe = None
    error_message = None  # Store validation errors

    if request.method == "POST":
        form = RecipeInputForm(request.POST)
        if form.is_valid():
            ingredients = [i.strip() for i in form.cleaned_data["ingredients"].split(",") if i.strip()]  # Clean input
            
            # Validate ingredients before calling OpenAI
            validation_error = validate_ingredients(ingredients)
            if validation_error:
                error_message = validation_error
            else:
                recipe, error_message = generate_recipe(ingredients, request.user)

    else:
        form = RecipeInputForm()

    return render(request, "recipes/recipe_detail.html", {"form": form, "recipe": recipe, "error_message": error_message})

