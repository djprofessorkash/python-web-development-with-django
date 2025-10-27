from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
def home(request):
    # return HttpResponse("<h1>Welcome to my portfolio!</h1><p>This is served by Django.</p>")
    context = {
        "name": "Kash",
        "interests": ["Coding", "Fitness", "Gaming", "Teaching"]
    }
    return render(request, "homepage/home.html", context)