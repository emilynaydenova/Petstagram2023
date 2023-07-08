import datetime

from django.contrib.auth import get_user_model
from django.db import models
from dateutil.relativedelta import relativedelta

from accounts.models import Profile
from common.validators import ValidateFileMaxSizeInMb

UserModel = get_user_model()
# Profile is moved to accounts models.py

# ------------------------------
#  many pets to one Profile
class Pet(models.Model):
    CAT = 'cat'
    DOG = 'dog'
    BUNNY = 'bunny'
    PARROT = 'parrot'
    FISH = 'fish'
    OTHER = 'other'

    # Constants
    PETS_CHOICES = [
        (CAT, 'Cat'),
        (DOG, 'Dog'),
        (BUNNY, 'Bunny'),
        (PARROT, 'Parrot'),
        (FISH, 'Fish'),
        (OTHER, 'Other'),
    ]

    NAME_MAX_LENGTH = 30

    # All pets' names should be unique for that user -> class Meta
    name = models.CharField(max_length=NAME_MAX_LENGTH, )

    type = models.CharField(
        max_length=max(len(x) for x, _ in PETS_CHOICES),
        choices=PETS_CHOICES,
    )

    DoB = models.DateField(blank=True, null=True,
                           # validators = [MinDateValidator(datetime.date(1920,1,1)),]
                           # validated in form with clean_date_of_birth
                           )

    # One-to-many relation
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE, )

    def __str__(self):
        return f'{self.name}'

    @property
    def age(self):
        # install python-dateutil
        years = relativedelta(datetime.date.today(), self.DoB).years
        return years

        # difference_in_years = relativedelta(end_date, start_date).years
    class Meta:
        # All pets' names should be unique for that user.
        unique_together = ('user', 'name')


# -----------------------------

class PetPhoto(models.Model):
    # To even work with the ImageField you need the Pillow package.
    # media files
    # https://nemecek.be/blog/79/working-with-django-imagefield
    photoFile = models.ImageField(upload_to='',
                                  validators=[ValidateFileMaxSizeInMb(max_size=5)],
                                  # validate_file_max_size_in_mb(5), #-> model.Forms

                                  )

    description = models.TextField(blank=True, null=True, )
    # when a picture is created (only)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, )

    likes = models.PositiveIntegerField(default=0, )
    # likes = models.ForeignKey('Like',on_delete=models.CASCADE)

    # tag at least one of their pets in model.Forms
    tagged_pets = models.ManyToManyField(Pet, )  # validate at least one pet
    #
    # CustomUser <-> PetPhotos
    # One-to-many relation
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE, )

    class Meta:
        ordering = ['created']

    #
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/

    def __str__(self):
        return self.description
#
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/
