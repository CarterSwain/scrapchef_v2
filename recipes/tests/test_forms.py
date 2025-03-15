from django.test import TestCase
from recipes.forms import RecipeInputForm

class RecipeInputFormTest(TestCase):
    """Tests for the RecipeInputForm."""

    def test_form_valid_input(self):
        """Ensure the form is valid with proper input."""
        form_data = {"ingredients": "chicken, garlic, olive oil"}
        form = RecipeInputForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_input(self):
        """Ensure the form is invalid if empty."""
        form = RecipeInputForm(data={"ingredients": ""})
        self.assertFalse(form.is_valid())

    def test_form_placeholder(self):
        """Check that the form's placeholder text is correct."""
        form = RecipeInputForm()
        self.assertEqual(form.fields["ingredients"].widget.attrs["placeholder"], "e.g. chicken, garlic, olive oil")
