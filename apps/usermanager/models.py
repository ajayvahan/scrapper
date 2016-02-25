"""Models for usermanager app."""


from django.db import models
from django.contrib.auth.models import User
from apps import constants as con
import datetime

# Create your models here.


def generate_filename(self, filename):
    """Used for handling upload file."""
    # set URL.
    url = "static/uploads/%s/%s" % (self.pk, filename)
    return url


class UserDetail(models.Model):
    """Model to store user details."""

    # One-to-one relation with auth_user table
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    # Date fields.
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )

    # Char fields.
    marital = models.CharField(
        max_length=1, choices=con.MARITAL_CHOICES, null=True, blank=True
    )
    gender = models.CharField(
        max_length=1, choices=con.GENDER_CHOICES, null=True, blank=True
    )
    address = models.CharField(max_length=254, null=True, blank=True)
    street = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    phone = models.IntegerField(default=0, null=True, blank=True)
    extra_note = models.CharField(max_length=254, null=True, blank=True)

    # boolean fields.
    mail = models.BooleanField(default=False)
    message = models.BooleanField(default=False)
    phonecall = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    # image field.
    image = models.ImageField(
        upload_to='static/uploads/', null=True, blank=True
    )

    def __str__(self):
        """Value to return when object is called."""
        return self.city

class UserActivation(models.Model):
    """Model for storing user activation key."""
    # One-to-one relation with auth_user table
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username
