from django import forms
from .models import UserProfile

class IngredientPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["ingredients_to_avoid", "diet_preference"]
        widgets = {
            "ingredients_to_avoid": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Enter ingredients separated by commas.",
                "class": "w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-yellow-500 focus:outline-none"
            }),
            "diet_preference": forms.Select(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-yellow-500 focus:outline-none"
            }),
        }
