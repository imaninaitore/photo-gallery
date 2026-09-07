from django.urls import path

from django.contrib.auth.views import (
    LoginView,
    LogoutView
)

from . import views


urlpatterns = [

    # -------------------------
    # BASIC PAGES
    # -------------------------

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "gallery/",
        views.gallery,
        name="gallery"
    ),

    path(
        "gallery/<int:photo_id>/",
        views.photo_detail,
        name="photo_detail"
    ),


    # -------------------------
    # AUTHENTICATION
    # -------------------------

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        LoginView.as_view(
            template_name="login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),


    # -------------------------
    # PHOTO MANAGEMENT
    # -------------------------

    path(
        "upload/",
        views.upload_photo,
        name="upload_photo"
    ),

    path(
        "photo/<int:photo_id>/edit/",
        views.edit_photo,
        name="edit_photo"
    ),

    path(
        "photo/<int:photo_id>/delete/",
        views.delete_photo,
        name="delete_photo"
    ),


    # -------------------------
    # LIKES / DISLIKES
    # -------------------------

    path(
        "photo/<int:photo_id>/react/<str:reaction_type>/",
        views.react_photo,
        name="react_photo"
    ),


    # -------------------------
    # PROFILES
    # -------------------------

    path(
        "profile/<str:username>/",
        views.profile,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),

    path(
        "profile/password/",
        views.ChangePasswordView.as_view(),
        name="change_password"
    ),
]