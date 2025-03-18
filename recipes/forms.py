from django import forms

class RecipeInputForm(forms.Form):
    ingredients = forms.CharField(
        label="Enter Ingredients",
        widget=forms.Textarea(attrs={
            "placeholder": "e.g. chicken, garlic, olive oil",
            "class": "w-full max-w-md mx-auto p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500 resize-none"
        }),
        required=True
    )
