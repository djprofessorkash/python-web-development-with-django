# Day 5 — Cookbook Project: Model Relationships and Advanced ORM

This tutorial walks you through **Day 5** of the Cookbook project: building advanced models with relationships, understanding the Django ORM, and implementing CRUD functionality for recipes, chefs, ingredients, and tags. It includes the main curriculum and stretch goals implemented earlier.

---

## Goals

- Build advanced models with `ForeignKey` and `ManyToManyField` relationships
- Use Django ORM for querying and filtering
- Display related data in templates
- Implement basic CRUD actions
- Introduce simple stretch goals for filtering and related data

---

## 1. Project Setup

Assuming you already have a Django project and a `recipes` app, ensure your directory structure looks like this:

```
cookbook/
├── manage.py
├── cookbook/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── recipes/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/recipes/
```

Add `'recipes'` to `INSTALLED_APPS` in `cookbook/settings.py`.

---

## 2. Create Models with Relationships

Edit `recipes/models.py`:

```python
from django.db import models

class Chef(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations recipes
python manage.py migrate
```

---

## 3. Register Models in Admin

**`recipes/admin.py`**

```python
from django.contrib import admin
from .models import Chef, Ingredient, Tag, Recipe

admin.site.register(Chef)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
```

Test in `/admin` to create sample chefs, ingredients, tags, and recipes.

---

## 4. Implement Views

**`recipes/views.py`**

```python
from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.core.paginator import Paginator


def recipe_list(request):
    qs = Recipe.objects.select_related('chef').prefetch_related('ingredients', 'tags').all()

    tag = request.GET.get('tag')
    ingredient = request.GET.get('ingredient')
    chef = request.GET.get('chef')
    q = request.GET.get('q')

    if tag:
        qs = qs.filter(tags__name__iexact=tag)
    if ingredient:
        qs = qs.filter(ingredients__name__iexact=ingredient)
    if chef:
        qs = qs.filter(chef__name__icontains=chef)
    if q:
        qs = qs.filter(title__icontains=q)

    qs = qs.distinct()

    paginator = Paginator(qs, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/recipe_list.html', {'page_obj': page_obj})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
```

---

## 5. Configure URLs

**`recipes/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
]
```

Include in `cookbook/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
]
```

---

## 6. Templates

Create templates in `recipes/templates/recipes/`:

- **`recipe_list.html`**
- **`recipe_detail.html`**

Include loops to display related ingredients, tags, and chef names. Use `{% if recipe.chef %}{{ recipe.chef.name }}{% else %}—{% endif %}` for safe rendering.

---

## 7. Stretch Goals

1. Display publisher and genre info (if added) in recipe details.
2. Implement search functionality with query parameters (`?q=term`).
3. Use a shared `base.html` template for consistent styling.

---

## 8. Test

1. Run the server: `python manage.py runserver`
2. Navigate to `/recipes/` to view the recipe list.
3. Navigate to `/recipes/<pk>/` for details.
4. Test filters, search, and pagination.

---

This completes **Day 5** of the **Python for Web Development** course and the first part of the Cookbook project.

---

### Recommended Stretch Challenges

#### 1. Ingredient Categories
- Add a Category model for ingredients (e.g., Vegetables, Proteins, Spices).
- Add a ForeignKey from Ingredient to Category.
- Display the category alongside ingredients in recipe detail pages.
(No change to Recipe model needed, safe for DB.)

#### 2. Recipe Difficulty Level
- Add a difficulty property (choices: Easy, Medium, Hard) to Recipe using CharField + choices.
- Display difficulty in list and detail pages.
- Add filtering by difficulty in the recipe list view.

#### 3. Advanced Query Practice
- Create a custom manager on Recipe called Recipe.objects.public() to filter is_public=True.
- Add a template snippet that lists all recipes using the custom manager.

#### 4. Bonus Template Exercise
- Use regroup to group recipes in the list page by chef.
- Display each chef as a heading, with their recipes underneath.

