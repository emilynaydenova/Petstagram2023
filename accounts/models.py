from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from accounts.managers import CustomUserManager
from common.validators import validate_only_letters

"""
1. Create model extending User model. -> CustomUser
2. Configure model in settings -> AUTH_USER_MODEL = 'accounts.CustomUser'
3. Create user manager for our model -> managers.py
"""




# https://testdriven.io/blog/django-custom-user-model/

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 25
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )
    # password comes from AbstractBaseUser
    date_joined = models.DateTimeField(auto_now_add=True, )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser comes from PermissionsMixin

    # says to AbstractBaseUser how to identify the user
    USERNAME_FIELD = 'username'  # can be email,phone etc.

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    DO_NOT_SHOW = 'DO_NOT_SHOW'

    GENDERS = [
        #  to db / to frontend
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (DO_NOT_SHOW, "Do not show")
    ]

    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    # Required fields
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            # builtin ORM validator - it is a class and has args
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),

            # custom validator - function reference ->
            # arg is the field from which is called by Django
            validate_only_letters,
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
    )
    # link to URL -> there is built-in URL validator
    pictureURL = models.URLField()  # = CharField + URL validation

    # Not required fields
    DoB = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        blank=True, null=True)

    # new in CBV
    user = models.OneToOneField(
        to=CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    # Properties
    @property  # to use in template
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
