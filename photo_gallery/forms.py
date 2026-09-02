# Import Django's forms system.
# This lets us create HTML forms using Python.
from django import forms

# Import Django's built-in User model.
# This model already contains username, email and password.
from django.contrib.auth.models import User


# Create our own registration form.
# ModelForm means Django will connect this form to a database model.
class RegisterForm(forms.ModelForm):

    # Create a password field.
    # PasswordInput hides the password while the user types.
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    # Create a second password field.
    # The user will type their password again to confirm it.
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    # Tell Django which model this form is connected to.
    class Meta:
        model = User

        # These are the fields we want the user to fill in.
        fields = ["username", "email", "password"]

    # This method checks the submitted form data.
    def clean(self):

        # First let Django perform its normal validation.
        cleaned_data = super().clean()

        # Get the first password from the form.
        password = cleaned_data.get("password")

        # Get the confirmation password from the form.
        password2 = cleaned_data.get("password2")

        # Check whether both passwords were entered
        # and whether they are different.
        if password and password2 and password != password2:

            # Tell the user that the passwords don't match.
            raise forms.ValidationError(
                "Passwords do not match."
            )

        # Return the cleaned data.
        return cleaned_data

    # This method controls how the user is saved.
    def save(self, commit=True):

        # Get the User object created by ModelForm.
        # commit=False means don't save it yet.
        user = super().save(commit=False)

        # IMPORTANT:
        # set_password() hashes the password before saving it.
        # We should NEVER save a user's plain password directly.
        user.set_password(
            self.cleaned_data["password"]
        )

        # If commit is True, save the user to the database.
        if commit:
            user.save()

        # Return the newly created user.
        return user