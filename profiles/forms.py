from django import forms
from .models import UserProfile

class IngredientPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["ingredients_to_avoid", "diet_preference"]
        widgets = {
            "ingredients_to_avoid": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter ingredients separated by commas."}),
            "diet_preference": forms.Select(),
        }
