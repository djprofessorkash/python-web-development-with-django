from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'page_title': 'Welcome to PyCafé!',
        'intro': 'Try our programming pastries and code-curated coffee!'
    }
    return render(request, 'menu/home.html', context)

def about(request):
    context = {
        'page_title': 'About PyCafé',
        'story': 'Founded in 2025, PyCafé is a cozy community for coffee enthusiasts and coding practitioners to come together!'
    }
    return render(request, 'menu/about.html', context)

def menu_page(request):
    menu_items = [
        {'category': 'Coding Coffee', 'name': 'Espresso', 'price': 3.50},
        {'category': 'Coding Coffee', 'name': 'Macchiato', 'price': 4.75},
        {'category': 'Technical Tea', 'name': 'Green Tea', 'price': 3.25},
        {'category': 'Technical Tea', 'name': 'Chai Latte', 'price': 3.75},
        {'category': 'Programming Pastries', 'name': 'Croissant', 'price': 4.95},
        {'category': 'Programming Pastries', 'name': 'Cinnamon Roll', 'price': 6.00},
    ]

    context = {
        'page_title': 'Our Menu',
        'menu_items': menu_items,
    }
    return render(request, 'menu/menu.html', context)

def specials(request):
    specials_data = [
        {'name': 'Python Spice Latte', 'desc': 'A seasonal favorite with cinnamon, pumpkin spice, nutmeg. Oh, and some Python programming.', 'price': 7.25},
        {'name': 'Functional Frappuccino ', 'desc': 'Caramel syrup mixed in coffee, milk, and ice, with just a hint of custom functions.', 'price': 6.10},
        {'name': 'Vanilla Code Brew', 'desc': 'Chilled cold brew topped with vanilla ice cream... and some decadent documentation.', 'price': 5.50},
    ]
    context = {
        'page_title': "Today's Specials",
        'specials': specials_data,
    }
    return render(request, 'menu/specials.html', context)

def contact(request):
    context = {
        'page_title': 'Contact Us',
        'message': "We'd love to hear from you! Send us a message below."
    }
    return render(request, 'menu/contact.html', context)
