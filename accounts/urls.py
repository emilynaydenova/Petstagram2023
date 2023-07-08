from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from accounts.views import UserLoginView, UserRegisterView, ChangeUserPasswordView, ProfileDetailsView, UserLogoutView, \
    EditProfileView, DeleteProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),

    path('edit-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),

    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name="profile details"),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name="edit profile"),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name="delete profile"),
]
