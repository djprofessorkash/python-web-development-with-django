from django import forms
from .models import Recipe, Chef, Ingredient, Tag

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "chef", "ingredients", "tags", "instructions", "cook_time_in_minutes", "difficulty"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 6}),
            "ingredients": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }