# Day 7 — Cookbook Project: Class-Based and Generic Views

This tutorial walks you through **Day 7** of the Cookbook project: converting function-based views to class-based views (CBVs) and leveraging Django's generic views to simplify CRUD operations. Stretch goals from previous days are included.

---

## Goals

- Understand class-based views vs. function-based views
- Implement generic views for list, detail, create, update, and delete
- Ensure authentication and authorization is respected in CBVs
- Maintain visibility filtering for public/private recipes

---

## 1. Update Views to Class-Based

**`recipes/views.py`**

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Recipe

# Recipe list with pagination and filtering
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'page_obj'
    paginate_by = 8

    def get_queryset(self):
        qs = Recipe.objects.select_related('chef').prefetch_related('ingredients', 'tags').all()
        tag = self.request.GET.get('tag')
        ingredient = self.request.GET.get('ingredient')
        chef = self.request.GET.get('chef')
        q = self.request.GET.get('q')

        if tag:
            qs = qs.filter(tags__name__iexact=tag)
        if ingredient:
            qs = qs.filter(ingredients__name__iexact=ingredient)
        if chef:
            qs = qs.filter(chef__name__icontains=chef)
        if q:
            qs = qs.filter(title__icontains=q)

        if self.request.user.is_authenticated:
            qs = qs.filter(Q(is_public=True) | Q(chef__user=self.request.user)).distinct()
        else:
            qs = qs.filter(is_public=True).distinct()

        return qs

# Recipe detail view
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

# Recipe create view
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'tags', 'is_public']
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.chef = self.request.user.chef
        return super().form_valid(form)

# Recipe update view
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'tags', 'is_public']
    template_name = 'recipes/recipe_form.html'

    def test_func(self):
        recipe = self.get_object()
        return recipe.chef.user == self.request.user

# Recipe delete view
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def test_func(self):
        recipe = self.get_object()
        return recipe.chef.user == self.request.user
```

---

## 2. Update URLs

**`recipes/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('add/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe_edit'),
    path('<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
]
```

---

## 3. Templates

- `recipe_list.html` remains mostly the same
- `recipe_detail.html` displays recipe with ingredients and tags
- `recipe_form.html` used for both create/update views
- `recipe_confirm_delete.html` added for deletion confirmation

Use `{% extends 'recipes/base.html' %}` in all templates for consistent layout.

---

## 4. Authentication & Authorization Checks

- LoginRequiredMixin ensures only logged-in users can create/edit/delete recipes
- UserPassesTestMixin ensures users can only modify their own recipes
- Visibility filtering from Day 6 is preserved in `get_queryset()` for the list view

---

## 5. Stretch Goals Recap

- Password reset, staff dashboard, public/private recipes (Day 6 stretch goals) all continue to function with CBVs
- Pagination and search remain functional in `RecipeListView`
- Base template styling and dynamic content blocks remain consistent

---

## 6. Test Everything

- List view: `/recipes/`
- Detail view: `/recipes/<pk>/`
- Create: `/recipes/add/`
- Update: `/recipes/<pk>/edit/`
- Delete: `/recipes/<pk>/delete/`
- Verify visibility filters and login restrictions
- Staff users can access stats dashboard

---

This completes **Day 7** of the **Python for Web Development** course and the third part of the Cookbook project.

---

### Recommended Stretch Challenges

#### 1. Custom `ListView` Pagination Control
- Add a GET parameter `?per_page=` to allow the user to choose 4, 8, or 12 recipes per page.
- Modify `get_paginate_by` in `RecipeListView` to handle this.

#### 2. Recipe Sorting
- Add sorting by title or `created_at` using query parameters (`?sort=title`).
- Use CBV `get_queryset` overrides for sorting without touching templates too much.

#### 3. Advanced `UpdateView`
- Allow editing only certain fields (like title and description) for normal users.
- Admin users can edit all fields including `is_public` and tags.

#### 4. Mixins
- Create a reusable mixin `OwnerRequiredMixin` that enforces ownership on update/delete views.
- Refactor `RecipeUpdateView` and `RecipeDeleteView` to use it.