from django.contrib import admin

from accounts.models import Profile
from app.models import Pet, PetPhoto


# Register your models here.
class PetInLineAdmin(admin.StackedInline):
    model = Pet


#
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #     inlines = (PetInLineAdmin,)  # to include user's Pets via FK
    list_display = ('first_name', 'last_name')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    pass
