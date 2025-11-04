from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Recipe, RecipeImage, Chef, Ingredient, Tag

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "chef", "ingredients", "tags", "instructions", "cook_time_in_minutes", "difficulty", "is_public", "image"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 6}),
            "ingredients": forms.CheckboxSelectMultiple(),
            "tags": forms.CheckboxSelectMultiple(),
        }

RecipeImageFormSet = forms.modelformset_factory(
    RecipeImage,
    fields=("image",),
    extra=3,
)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")