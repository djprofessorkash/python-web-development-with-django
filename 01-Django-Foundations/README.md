# Day One — Django Foundations: Personal Portfolio

Welcome to **Python for Web Development with Django**! In Day One of this course, we'll focus on learning the fundamentals. 

In this walkthrough, we'll build a **Personal Portfolio** using Django. This tutorial assumes you have Python 3 installed and are comfortable with basic command-line operations.

---

## Goals

- Set up a Python virtual environment.
- Install Django and start a project and app.
- Understand Django's project/app structure.
- Create URL routes, views, and templates.
- Run the development server and view your portfolio locally.

---

## 1. Create a project directory and virtual environment.

Open your terminal and run the following commands:

```bash
mkdir portfolio
cd portfolio
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate

# Upgrade pip and install Django
pip install --upgrade pip
pip install django
```

**Why?** Using a virtual environment keeps dependencies isolated per project.

---

## 2. Start a new Django project and application.

```bash
# Create the Django project (`portfolio` is the project folder).
django-admin startproject portfolio .

# Create a new application called `homepage`.
python manage.py startapp homepage
```

You should now have this structure:

```
portfolio/
├── manage.py
├── portfolio/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── homepage/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    └── views.py
```

---

## 3. Register the `homepage` app

Open `portfolio/settings.py` and add `'homepage'` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',  # <-- Add this line!
]
```

Save the file.

---

## 4. Create application-level URLs.

Create a new file called `homepage/urls.py` and add:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
]
```

Now hook these into the project-level URLs.

Open `portfolio/urls.py` and modify:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
]
```

This delegates root URL routing to the `portfolio` app.

---

## 5. Create basic views

Edit `homepage/views.py` and add the following views:

```python
from django.shortcuts import render


def home(request):
    context = {
        'page_title': 'Home',
        'intro': 'Welcome to my portfolio! Here are some selected projects.'
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    context = {
        'page_title': 'About',
        'bio': 'I am a developer who loves Python and web development.'
    }
    return render(request, 'portfolio/about.html', context)


def projects(request):
    projects_data = [
        {'name': 'Weather App', 'tech': 'Django, API', 'desc': 'A small weather dashboard.'},
        {'name': 'Task Manager', 'tech': 'Django, JS', 'desc': 'A to-do CRUD app.'},
        {'name': 'Portfolio', 'tech': 'HTML, Django', 'desc': 'A personal site.'},
    ]
    context = {
        'page_title': 'Projects',
        'projects': projects_data
    }
    return render(request, 'homepage/projects.html', context)
```

These views pass context dictionaries to templates for rendering dynamic content.

---

## 6. Add templates and template inheritance

Create the templates directory and files:

```
mkdir -p homepage/templates/homepage
```

Create `homepage/templates/homepage/base.html` with a simple base layout:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}{{ page_title }} | My Portfolio{% endblock %}</title>
    <style>
        body { font-family: sans-serif; margin: 2rem; }
        nav { margin-bottom: 1rem; }
        a { margin-right: 1rem; text-decoration: none; color: #1a73e8; }
        .container { padding: 1rem; background: #fff; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <nav>
        <a href="{% url 'home' %}">Home</a>
        <a href="{% url 'about' %}">About</a>
        <a href="{% url 'projects' %}">Projects</a>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

Create `homepage/templates/homepage/home.html`:

```html
{% extends 'homepage/base.html' %}

{% block content %}
<h1>{{ page_title }}</h1>
<p>{{ intro }}</p>
{% endblock %}
```

Create `homepage/templates/homepage/about.html`:

```html
{% extends 'homepage/base.html' %}

{% block content %}
<h1>{{ page_title }}</h1>
<p>{{ bio }}</p>
{% endblock %}
```

Create `homepage/templates/homepage/projects.html`:

```html
{% extends 'homepage/base.html' %}

{% block content %}
<h1>{{ page_title }}</h1>
<ul>
    {% for project in projects %}
        <li>
            <strong>{{ project.name }}</strong> — <em>{{ project.tech }}</em><br>
            {{ project.desc }}
        </li>
    {% empty %}
        <li>No projects yet.</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

## 7. Run the development server

Start the server with:

```bash
python manage.py runserver
```

Open your browser and visit:

- http://127.0.0.1:8000/ — Home
- http://127.0.0.1:8000/about/ — About
- http://127.0.0.1:8000/projects/ — Projects

If you see your pages, congratulations — your first Django app is live locally!

---

## Troubleshooting tips

- If templates are not found, confirm that each template path is `homepage/templates/homepage/<template>.html` and `homepage` is in `INSTALLED_APPS`.
- If the dev server doesn't pick up changes, restart it.
- For syntax errors in templates, remember Django templates do not support inline Python expressions — use `{% if %}`, `{% for %}`, and template filters.

---

## Resources

- Django official tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Django templates: https://docs.djangoproject.com/en/stable/topics/templates/

---

Happy coding! 🎉

If you'd like, I can also export this file as a downloadable markdown file or create an instructor-facing version with timings and checkpoints.

