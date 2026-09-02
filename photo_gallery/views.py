from django.shortcuts import render,redirect
from .models import Photo
# Import the registration form we just created.
from .forms import RegisterForm

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

# REGISTER PAGE
# -------------------------

def register(request):

    # Check whether the user submitted the form.
    if request.method == "POST":

        # Put the submitted information into our form.
        form = RegisterForm(request.POST)

        # Check whether the submitted information is valid.
        if form.is_valid():

            # Save the new user to the database.
            form.save()

            # After registration, send the user to the login page.
            return redirect("login")

    else:

        # If the user is simply visiting the page,
        # create an empty registration form.
        form = RegisterForm()

    # Display register.html and send the form to it.
    return render(
        request,
        "register.html",
        {"form": form}
    )
