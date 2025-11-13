# Day 2 — Café Project: Apps, Routing, and Templates

This tutorial walks through **Day 2** of our Django learning path: building a simple café website using multiple apps, routing, and templates. The project focuses on modular development, URL configuration, and template rendering. 

---

## Goals

- Create a Django app within the `pycafe` project
- Configure URL routing for multiple pages
- Use templates and template inheritance
- Build a self-contained project demonstrating modular Django patterns

---

## 1. Project Setup

If you haven't already, create the project and activate your virtual environment:

```bash
django-admin startproject pycafe
cd pycafe
python -m venv venv
source venv/bin/activate    # macOS/Linux only
venv\Scripts\activate       # Windows only
pip install django
```

Start the Django development server to verify setup:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ to ensure the default Django page loads.

---

## 2. Create a New App

We'll create an app named `menu` to manage café menu items.

```bash
python manage.py startapp menu
```

Add `menu` to `INSTALLED_APPS` in `pycafe/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'menu',
]
```

---

## 3. Configure URL Routing

### Project URLs (`pycafe/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]
```

### App URLs (`menu/urls.py`)

Create `urls.py` in `menu/`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu_list, name='menu_list'),
]
```

---

## 4. Create Views (`menu/views.py`)

```python
from django.shortcuts import render

def home(request):
    return render(request, 'menu/home.html')


def about(request):
    return render(request, 'menu/about.html')


def menu_list(request):
    items = [
        {'name': 'Espresso', 'price': 2.5},
        {'name': 'Cappuccino', 'price': 3.5},
        {'name': 'Latte', 'price': 4.0},
    ]
    return render(request, 'menu/menu_list.html', {'items': items})
```

---

## 5. Templates

Create `menu/templates/menu/` folder. We'll have three templates: `home.html`, `about.html`, and `menu_list.html`. We'll also create a shared base template `base.html`.

### Base Template (`base.html`)

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}PyCafé{% endblock %}</title>
</head>
<body>
    <header>
        <h1>PyCafé</h1>
        <nav>
            <a href="{% url 'home' %}">Home</a> |
            <a href="{% url 'about' %}">About</a> |
            <a href="{% url 'menu_list' %}">Menu</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2025 PyCafé</p>
    </footer>
</body>
</html>
```

### Home Page (`home.html`)

```django
{% extends 'menu/base.html' %}

{% block title %}Home - PyCafé{% endblock %}

{% block content %}
<h2>Welcome to PyCafé!</h2>
<p>Enjoy our freshly brewed beverages and pastries.</p>
{% endblock %}
```

### About Page (`about.html`)

```django
{% extends 'menu/base.html' %}

{% block title %}About - PyCafé{% endblock %}

{% block content %}
<h2>About PyCafé</h2>
<p>PyCafé is your friendly neighborhood café serving coffee and code.</p>
{% endblock %}
```

### Menu Page (`menu_list.html`)

```django
{% extends 'menu/base.html' %}

{% block title %}Menu - PyCafé{% endblock %}

{% block content %}
<h2>Our Menu</h2>
<ul>
    {% for item in items %}
        <li>{{ item.name }} — ${{ item.price }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

## 6. Static Files (Optional)

Create `menu/static/menu/` and add CSS files, e.g., `style.css`. Link in `base.html`:

```django
<link rel="stylesheet" href="{% static 'menu/style.css' %}">
```

Enable `django.contrib.staticfiles` in `INSTALLED_APPS` (default) and run `python manage.py collectstatic` for production.

---

## 7. Run the Server

```bash
python manage.py runserver
```

Visit the following URLs to confirm:  

- Home: http://127.0.0.1:8000/  
- About: http://127.0.0.1:8000/about/  
- Menu: http://127.0.0.1:8000/menu/  

Confirm that the navigation links work and templates render correctly.

---

## 8. Additional Goals

1. Add a `Contact` page with a simple contact form (does not require database).  
2. Add a dynamic `specials` list fetched from a JSON file and rendered in the menu page.  
3. Apply basic CSS styling to make the navigation bar and footer visually distinct.  
4. Add a reusable template block `{% block sidebar %}` in `base.html` to allow future sidebars for promotions or events.  

---

This completes **Day 2** of your Django learning series, building a fully functional café project with apps, routing, and templates, ready for expansion in subsequent days.

