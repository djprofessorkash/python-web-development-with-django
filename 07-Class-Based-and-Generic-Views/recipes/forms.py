from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Recipe, Chef, Ingredient, Tag

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "chef", "ingredients", "tags", "instructions", "cook_time_in_minutes", "difficulty", "is_public"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 6}),
            "ingredients": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")