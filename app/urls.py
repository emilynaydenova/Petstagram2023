from django.urls import path

from app.views.generic import HomeView, DashboardView
from app.views.pet_photos import CreatePetPhotoView, EditPetPhotoView, PetPhotoDetailsView,\
    like_pet_photo, DeletePetPhotoView
from app.views.pets import CreatePetView, EditPetView, DeletePetView

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),

    # path('profile/', show_profile, name="profile details"),
    # path('profile/create/', create_profile, name="create profile"),
    # path('profile/edit/<int:pk>/', edit_profile, name="edit profile"),
    # path('profile/delete/<int:pk>/', delete_profile, name="delete profile"),
    #

    path('pet/create/', CreatePetView.as_view(), name="create pet"),
    path('pet/edit/<int:pk>/', EditPetView.as_view(), name="edit pet"),
    path('pet/delete/<int:pk>/', DeletePetView.as_view(), name="delete pet"),

    path('photo/add',CreatePetPhotoView.as_view(), name="add pet photo"),
    path('photo/edit/<int:pk>/',EditPetPhotoView.as_view(), name="edit pet photo"),
    path('photo/delete/<int:pk>/',DeletePetPhotoView.as_view(), name="delete pet photo"),
    path('photo/details/<int:pk>/', PetPhotoDetailsView.as_view(), name='pet photo details'),
    path('photo/like/<int:pk>', like_pet_photo, name="like pet photo"),
]


# Dashboard Page: http://127.0.0.1:8000/dashboard/
# Profile Page: http://127.0.0.1:8000/profile/
# Photo Details Page: http://127.0.0.1:8000/photo/details/photo_id/
