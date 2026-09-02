from django.shortcuts import render
from .models import Photo

# Create your views here.
def home(request):
    return render(request, "home.html")
def about(request):
    return render(request, "about.html")
def gallery(request):
    photos = Photo.objects.all()

    return render(request, "gallery.html", {"photos": photos})