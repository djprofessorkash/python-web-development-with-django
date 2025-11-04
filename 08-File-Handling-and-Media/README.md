# Day 8 — Cookbook Project: File Handling and Media

This tutorial walks you through **Day 8** of the Cookbook project: adding media support, handling file uploads, creating galleries for recipes, and implementing related stretch goals such as thumbnail generation and file cleanup.

---

## Goals

- Add image uploads for recipes
- Display images in recipe templates
- Handle multiple images per recipe (gallery)
- Validate file types
- Automatically resize images for performance
- Clean up image files on deletion

---

## 1. Update Models for Media

**`recipes/models.py`**

```python
from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
import os

class RecipeImage(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='recipes/gallery/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img_path = self.image.path
        img = Image.open(img_path)
        max_size = (800, 800)
        img.thumbnail(max_size)
        img.save(img_path)
```

Run migrations:

```bash
python manage.py makemigrations recipes
python manage.py migrate
```

---

## 2. Register Inline in Admin

**`recipes/admin.py`**

```python
from django.contrib import admin
from .models import Recipe, RecipeImage

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title','chef','is_public','created_at')
    inlines = [RecipeImageInline]
```

Now multiple images can be added to a recipe in the admin.

---

## 3. Display Images in Templates

**`recipes/templates/recipes/recipe_detail.html`**

```django
{% if recipe.images.all %}
  <div class="gallery">
    {% for image in recipe.images.all %}
      <img src="{{ image.image.url }}" alt="{{ recipe.title }}" style="width:200px; height:auto; margin:5px;">
    {% endfor %}
  </div>
{% endif %}
```

---

## 4. Optional: Multi-Image Upload via Formset

**`recipes/forms.py`**

```python
from django.forms import modelformset_factory
from .models import RecipeImage

RecipeImageFormSet = modelformset_factory(
    RecipeImage,
    fields=('image',),
    extra=3
)
```

Use `RecipeImageFormSet` in the `recipe_create` and `recipe_edit` views for multi-image uploads.

---

## 5. File Cleanup on Delete

**`recipes/models.py`**

```python
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=RecipeImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
```

This ensures files are removed from disk when the database record is deleted.

---

## 6. Test Everything

1. Run `python manage.py runserver`
2. Navigate to a recipe detail page
3. Upload multiple images via admin or formset
4. Confirm gallery displays correctly
5. Delete images and ensure files are removed from `media/`
6. Confirm thumbnails are resized to 800x800 max

---

This completes **Day 8** of the **Python for Web Development** course and the fourth and final part of the cookbook project, covering all core media functionality and stretch goals.

---

### Recommended Stretch Challenges

#### 1. Recipe Image Gallery Lightbox
- Add JavaScript to open images in a lightbox/modal on click.
- Keep HTML structure intact; no backend changes needed.

#### 2. Multiple Upload Validation
- Validate file size and type client-side using JS.
- Display user-friendly error messages if a file is too large or invalid.

#### 3. Image Ordering
- Add an order field to RecipeImage (integer).
- Display images in that order in the gallery.
- Implement drag-and-drop ordering in admin using django-admin-sortable2 or similar (only if students want an advanced stretch).

#### 4. Dynamic Cleanup
- Add management command to find orphaned image files (on disk but not in DB).
- Output a list and optionally delete them.