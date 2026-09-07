from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (
    Photo,
    Tag,
    Profile,
    Reaction
)


class AuthenticationTests(TestCase):
    """
    Tests user registration and authentication.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )


    def test_user_can_login(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword123"
            }
        )

        # Successful login redirects the user.
        self.assertEqual(
            response.status_code,
            302
        )


    def test_wrong_password_fails(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "wrongpassword"
            }
        )

        # Login page is displayed again.
        self.assertEqual(
            response.status_code,
            200
        )


class PhotoTests(TestCase):
    """
    Tests the Photo model.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="photographer",
            password="password123"
        )


    def test_photo_belongs_to_user(self):

        photo = Photo.objects.create(
            title="Test Photo",
            description="A test image",
            owner=self.user,
            image="photos/test.jpg"
        )

        self.assertEqual(
            photo.owner,
            self.user
        )


    def test_photo_title_is_saved(self):

        photo = Photo.objects.create(
            title="Beautiful Sunset",
            description="Sunset photo",
            owner=self.user,
            image="photos/sunset.jpg"
        )

        self.assertEqual(
            photo.title,
            "Beautiful Sunset"
        )


class TagTests(TestCase):
    """
    Tests the tag system.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="user",
            password="password123"
        )

        self.photo = Photo.objects.create(
            title="Nature",
            description="Nature photo",
            owner=self.user,
            image="photos/nature.jpg"
        )


    def test_tag_can_be_added_to_photo(self):

        tag = Tag.objects.create(
            name="nature"
        )

        self.photo.tags.add(tag)

        self.assertIn(
            tag,
            self.photo.tags.all()
        )


class ReactionTests(TestCase):
    """
    Tests likes and dislikes.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="user",
            password="password123"
        )

        self.photo = Photo.objects.create(
            title="Test",
            description="Test photo",
            owner=self.user,
            image="photos/test.jpg"
        )


    def test_user_can_like_photo(self):

        reaction = Reaction.objects.create(
            user=self.user,
            photo=self.photo,
            reaction="like"
        )

        self.assertEqual(
            reaction.reaction,
            "like"
        )

        self.assertEqual(
            self.photo.like_count,
            1
        )


    def test_user_can_dislike_photo(self):

        reaction = Reaction.objects.create(
            user=self.user,
            photo=self.photo,
            reaction="dislike"
        )

        self.assertEqual(
            reaction.reaction,
            "dislike"
        )

        self.assertEqual(
            self.photo.dislike_count,
            1
        )


class ViewTests(TestCase):
    """
    Tests important pages.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )


    def test_home_page_loads(self):

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_gallery_page_loads(self):

        response = self.client.get(
            reverse("gallery")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_login_required_for_upload(self):

        response = self.client.get(
            reverse("upload_photo")
        )

        # Anonymous users should be redirected
        # to the login page.
        self.assertEqual(
            response.status_code,
            302
        )


    def test_logged_in_user_can_access_upload(self):

        self.client.login(
            username="testuser",
            password="password123"
        )

        response = self.client.get(
            reverse("upload_photo")
        )

        self.assertEqual(
            response.status_code,
            200
        )


class ProfileTests(TestCase):
    """
    Tests the profile functionality.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="profileuser",
            password="password123"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            bio="I love photography."
        )


    def test_profile_exists(self):

        self.assertEqual(
            self.profile.user.username,
            "profileuser"
        )


    def test_profile_page_loads(self):

        self.client.login(
          username="profileuser",
          password="password123")

        response = self.client.get(
            reverse(
                "profile",
                args=["profileuser"]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )