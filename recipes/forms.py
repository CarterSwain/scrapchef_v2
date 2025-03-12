from django import forms

class RecipeInputForm(forms.Form):
    ingredients = forms.CharField(
        label="Enter Ingredients",
        widget=forms.Textarea(attrs={"placeholder": "e.g. chicken, garlic, olive oil"}),
        required=True
    )
