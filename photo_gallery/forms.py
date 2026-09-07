from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from .models import Photo, Profile


class RegisterForm(forms.ModelForm):
    """
    Form used to create a new user account.
    """

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password"
        ]

    def clean(self):
        """
        clean() lets us perform validation involving
        more than one field.

        We use it to make sure both passwords match.
        """

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2:

            if password != password2:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):
        """
        IMPORTANT:

        We use set_password() instead of directly saving
        the password.

        set_password() hashes the password before storing it.
        """

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user


class PhotoForm(forms.ModelForm):
    """
    Form used when uploading or editing a photo.
    """

    # The user types tags like:
    #
    # nature, sunset, photography
    #
    # We convert these into Tag objects in the view.
    tags_input = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separate tags using commas."
    )

    class Meta:
        model = Photo

        fields = [
            "title",
            "description",
            "image"
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 5
                }
            )
        }


class UserUpdateForm(forms.ModelForm):
    """
    Allows the user to update their username and email.
    """

    class Meta:
        model = User

        fields = [
            "username",
            "email"
        ]


class ProfileUpdateForm(forms.ModelForm):
    """
    Allows the user to update their profile information.
    """

    class Meta:
        model = Profile

        fields = [
            "bio",
            "profile_picture"
        ]