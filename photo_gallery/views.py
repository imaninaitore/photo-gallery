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

#add detail view means get photo with  this ID and send to detail page
def photo_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)

    return render(request, "photo_detail.html", {"photo": photo})