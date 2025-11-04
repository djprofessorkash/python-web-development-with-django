# Day 6 — Cookbook Project: Authentication and Authorization

This tutorial walks you through **Day 6** of the Cookbook project: adding user accounts, authentication, authorization, and access control to the app. Includes the main curriculum and previously implemented stretch goals.

---

## Goals

- Add user authentication (signup, login, logout)
- Restrict recipe editing/creation to authenticated users
- Implement chef-user relationship
- Add visibility controls for public/private recipes
- Implement password reset and password change flows

---

## 1. Update Models for Auth

In `recipes/models.py`:

```python
from django.contrib.auth.models import User

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name
```

Run migrations:

```bash
python manage.py makemigrations recipes
python manage.py migrate
```

---

## 2. Add User Forms

**`recipes/forms.py`**

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
```

---

## 3. Authentication Views

**`recipes/views.py`**

```python
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = SignUpForm()
    return render(request, 'recipes/signup.html', {'form': form})
```

For login/logout, use Django's built-in views in `urls.py`.

---

## 4. Recipe Permissions

Update list and detail views to filter by `is_public` and ownership:

```python
from django.db.models import Q

recipes = Recipe.objects.filter(
    Q(is_public=True) | Q(chef__user=request.user)
) if request.user.is_authenticated else Recipe.objects.filter(is_public=True)
```

Ensure only recipe owners can edit/delete their recipes.

---

## 5. Templates for Auth

**signup.html**

```django
{% extends 'recipes/base.html' %}
{% block content %}
<h1>Sign Up</h1>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign Up</button>
</form>
{% endblock %}
```

Add login/logout templates similarly using Django's built-in forms.

---

## 6. Password Reset and Change (Stretch Goal 1)

- Add paths for `password_change`, `password_change_done`, `password_reset`, `password_reset_done`, `password_reset_confirm`, `password_reset_complete`
- Use Django's built-in auth views

Update templates accordingly and ensure redirects go to proper URLs to avoid 404 errors.

---

## 7. Staff-Only Dashboard (Stretch Goal 2)

**View in `views.py`**

```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def recipes_stats(request):
    total_recipes = Recipe.objects.count()
    public_recipes = Recipe.objects.filter(is_public=True).count()
    return render(request, 'recipes/stats.html', {
        'total_recipes': total_recipes,
        'public_recipes': public_recipes
    })
```

Add template `stats.html` to show counts.

---

## 8. Public/Private Recipe Visibility (Stretch Goal 3)

Update `recipe_list` view to filter recipes based on authentication and ownership (already included in Step 4). Update templates to indicate if a recipe is private.

---

## 9. URLs

**`recipes/urls.py`**

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='recipe_list'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('stats/', views.recipes_stats, name='recipes_stats'),
]
```

---

## 10. Test Everything

- Sign up and log in
- Create/edit recipes and verify ownership restrictions
- Test public/private recipe visibility
- Test password reset and change
- Access staff dashboard as a staff user

---

This completes **Day 6** of the **Python for Web Development** course and the second part of the cookbook project, including all main functionality and stretch goals.

---

### Recommended Stretch Challenges

#### 1. Profile Picture for Chefs
- Add a `profile_image` field to the Chef model (optional `ImageField`).
- Display chef images on recipe detail pages and admin list.
- Validate file type and size without affecting main workflow.

#### 2. Email Confirmation Simulation
- Simulate email confirmation by creating a confirmed `BooleanField` on the user profile.
- Allow access to certain pages only if `confirmed=True`.
- Use a toggle in the admin to mark users confirmed.

#### 3. Custom Permissions
- Create a permission like `can_mark_featured` on Recipe.
- Add a checkbox in the admin for featured recipes and display featured recipes on the homepage.

#### 4. Custom Decorators
- Write a custom decorator `@chef_required` to restrict certain views to authenticated chefs only.
- Apply it to a test view (e.g., `/my-favorite-recipes/`) without changing existing views.

