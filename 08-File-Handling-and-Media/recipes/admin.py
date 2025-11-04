from django.contrib import admin
from .models import Chef, Ingredient, Tag, Recipe, RecipeImage

@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "chef", "difficulty", "cook_time_in_minutes", "created_at")
    inlines = [RecipeImageInline]
    list_filter = ("difficulty", "tags")
    search_fields = ("title", "chef__name", "ingredients__name")
    filter_horizontal = ("ingredients", "tags")
