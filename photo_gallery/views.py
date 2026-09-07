from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .models import (
    Photo,
    Tag,
    Reaction,
    Profile
)

from .forms import (
    RegisterForm,
    PhotoForm,
    UserUpdateForm,
    ProfileUpdateForm
)


def home(request):
    """
    Homepage.

    We display the newest photos first.
    """

    photos = Photo.objects.order_by("-created_at")[:6]

    return render(
        request,
        "home.html",
        {
            "photos": photos
        }
    )


def about(request):
    """
    About page.
    """

    return render(
        request,
        "about.html"
    )


def gallery(request):
    """
    Displays all photos.

    If the user selects a tag, we only display
    photos containing that tag.

    Example:

    /gallery/?tag=nature
    """

    photos = Photo.objects.all()

    tag_name = request.GET.get("tag")

    if tag_name:

        photos = photos.filter(
            tags__name__iexact=tag_name
        )

    # Get all tags so we can display them
    # as filter buttons on the gallery page.
    tags = Tag.objects.all().order_by("name")

    return render(
        request,
        "gallery.html",
        {
            "photos": photos,
            "tags": tags,
            "selected_tag": tag_name
        }
    )


def photo_detail(request, photo_id):
    """
    Displays one specific photo.

    get_object_or_404() is safer than Photo.objects.get()
    because it automatically returns a 404 page if the
    photo doesn't exist.
    """

    photo = get_object_or_404(
        Photo,
        id=photo_id
    )

    return render(
        request,
        "photo_detail.html",
        {
            "photo": photo
        }
    )


def register(request):
    """
    Handles user registration.
    """

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            # Create the user's profile automatically.
            Profile.objects.create(
                user=user
            )

            # Log the user in immediately.
            login(
                request,
                user
            )

            return redirect("gallery")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


@login_required
def upload_photo(request):
    """
    Allows a logged-in user to upload a photo.
    """

    if request.method == "POST":

        # request.FILES is necessary because
        # the form contains an uploaded image.
        form = PhotoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            photo = form.save(
                commit=False
            )

            # VERY IMPORTANT:
            #
            # The photo belongs to the currently
            # logged-in user.
            #
            # This prevents users from pretending
            # another user uploaded the photo.
            photo.owner = request.user

            photo.save()

            # Process the tags typed by the user.
            save_tags(
                photo,
                form.cleaned_data["tags_input"]
            )

            return redirect(
                "photo_detail",
                photo_id=photo.id
            )

    else:

        form = PhotoForm()

    return render(
        request,
        "upload_photo.html",
        {
            "form": form
        }
    )


def save_tags(photo, tags_input):
    """
    Converts:

        nature, sunset, kenya

    into separate Tag objects.

    This function is used by both the upload
    and edit views.
    """

    # Remove spaces around commas.
    tag_names = [
        tag.strip().lower()
        for tag in tags_input.split(",")
        if tag.strip()
    ]

    # Remove existing tags first.
    photo.tags.clear()

    for tag_name in tag_names:

        # get_or_create means:
        #
        # If the tag exists -> use it.
        #
        # If it doesn't exist -> create it.
        #
        tag, created = Tag.objects.get_or_create(
            name=tag_name
        )

        photo.tags.add(tag)


@login_required
def edit_photo(request, photo_id):
    """
    Allows the owner of a photo to edit it.
    """

    photo = get_object_or_404(
        Photo,
        id=photo_id
    )

    # SECURITY CHECK:
    #
    # Only the person who owns the photo
    # can edit it.
    if photo.owner != request.user:

        return redirect(
            "photo_detail",
            photo_id=photo.id
        )

    if request.method == "POST":

        form = PhotoForm(
            request.POST,
            request.FILES,
            instance=photo
        )

        if form.is_valid():

            updated_photo = form.save()

            save_tags(
                updated_photo,
                form.cleaned_data["tags_input"]
            )

            return redirect(
                "photo_detail",
                photo_id=photo.id
            )

    else:

        # Convert existing Tag objects back into text
        # so the edit form can display them.
        existing_tags = ", ".join(
            photo.tags.values_list(
                "name",
                flat=True
            )
        )

        form = PhotoForm(
            instance=photo,
            initial={
                "tags_input": existing_tags
            }
        )

    return render(
        request,
        "edit_photo.html",
        {
            "form": form,
            "photo": photo
        }
    )


@login_required
def delete_photo(request, photo_id):
    """
    Deletes a photo.

    Only the owner can delete it.
    """

    photo = get_object_or_404(
        Photo,
        id=photo_id
    )

    if photo.owner != request.user:

        return redirect(
            "photo_detail",
            photo_id=photo.id
        )

    if request.method == "POST":

        photo.delete()

        return redirect("gallery")

    return render(
        request,
        "confirm_delete.html",
        {
            "photo": photo
        }
    )


@login_required
def react_photo(request, photo_id, reaction_type):
    """
    Handles likes and dislikes.

    reaction_type will be either:

        like

    or:

        dislike
    """

    photo = get_object_or_404(
        Photo,
        id=photo_id
    )

    # Only allow our two valid reaction types.
    if reaction_type not in ["like", "dislike"]:

        return redirect(
            "photo_detail",
            photo_id=photo.id
        )

    if request.method == "POST":

        reaction, created = Reaction.objects.get_or_create(
            user=request.user,
            photo=photo,
            defaults={
                "reaction": reaction_type
            }
        )

        if not created:

            # If the user clicks the same reaction again,
            # remove their reaction.
            if reaction.reaction == reaction_type:

                reaction.delete()

            else:

                # If they change from like to dislike
                # or dislike to like, update the existing record.
                reaction.reaction = reaction_type
                reaction.save()

    return redirect(
        "photo_detail",
        photo_id=photo.id
    )


@login_required
def profile(request, username):
    """
    Displays a user's profile and their photos.
    """

    user = get_object_or_404(
        User,
        username=username
    )

    photos = Photo.objects.filter(
        owner=user
    ).order_by("-created_at")

    # get_or_create makes this view safe even if
    # an old user does not have a Profile yet.
    profile_obj, created = Profile.objects.get_or_create(
        user=user
    )

    return render(
        request,
        "profile.html",
        {
            "profile_user": user,
            "profile": profile_obj,
            "photos": photos
        }
    )


@login_required
def edit_profile(request):
    """
    Allows the currently logged-in user
    to update their account/profile.
    """

    profile_obj, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_obj
        )

        if (
            user_form.is_valid()
            and profile_form.is_valid()
        ):

            user_form.save()
            profile_form.save()

            return redirect(
                "profile",
                username=request.user.username
            )

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=profile_obj
        )

    return render(
        request,
        "edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form
        }
    )


class ChangePasswordView(PasswordChangeView):
    """
    Django provides password-changing functionality for us.

    We don't need to manually create the password
    hashing system again.
    """

    template_name = "change_password.html"

    success_url = reverse_lazy(
        "gallery"
    )