from django.urls import path
from . import views

# Import Django's built-in login and logout views.
from django.contrib.auth.views import LoginView, LogoutView

# This list contains all URLs belonging to the photo_gallery app.

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('register/',views.register,name='register'),

    # Django's built-in LoginView handles login.
    
    # We tell it which HTML template to use.
    path( 'login/', LoginView.as_view(    template_name='login.html' ),name='login' ),

    # Django's built-in LogoutView handles logging out.
    path('logout/', LogoutView.as_view(), name='logout'),
]
