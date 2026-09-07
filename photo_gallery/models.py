from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    # One user can have one profile.
    # CASCADE means if the user is deleted, their profile is deleted too.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.TextField(
        blank=True,
        max_length=500
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Tag(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Photo(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="photos/"
    )

    # The person who uploaded the photo.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="photos"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    @property
    def like_count(self):

        return self.reactions.filter(
            reaction="like"
        ).count()

    @property
    def dislike_count(self):
        """
        Counts how many users disliked this photo.
        """

        return self.reactions.filter(
            reaction="dislike"
        ).count()


class Reaction(models.Model):

    REACTION_CHOICES = [
        ("like", "Like"),
        ("dislike", "Dislike"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    class Meta:
        # It prevents the same user from creating multiple reactions for the same photo.
        constraints = [
            models.UniqueConstraint(
                fields=["user", "photo"],
                name="one_reaction_per_user_per_photo"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.photo.title} - {self.reaction}"