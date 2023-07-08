from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from common.view_mixins import RedirectToDashboardMixin
from accounts.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from accounts.models import Profile
from app.models import Pet, PetPhoto


# Create your views here.

class UserRegisterView(RedirectToDashboardMixin, CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        # user => self.object
        # request => self.request
        login(self.request, self.object)
        return result


class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    # by default redirect to accounts/profile -> so must have:
    def get_success_url(self):
        """
        Determine the URL to redirect to when the form is successfully
        validated. Returns success_url by default.
        """
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(LogoutView):
    success_url = reverse_lazy('index')

    def get_success_url(self):
        """
        Determine the URL to redirect to when the form is successfully
        validated. Returns success_url by default.
        """
        if self.success_url:
            return self.success_url
        return super().get_success_url()


# from auth/views -> modify Password
class ChangeUserPasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.object is a Profile instance
        pets = Pet.objects.filter(user_id=self.object.user_id)

        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()

        total_pet_photos_count = pet_photos.count()
        total_likes_count = sum(pp.likes for pp in pet_photos)

        is_owner = (self.object.user_id == self.request.user.id)

        context.update({
            'pets': pets,
            'total_likes_count': total_likes_count,
            'total_pet_photos_count': total_pet_photos_count,
            'is_owner': is_owner,
        })

        return context


class EditProfileView(UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'
    form_class = EditProfileForm

    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class DeleteProfileView(DeleteView):
    # !!!
    model = get_user_model()  # delete user and on_cascade -> profile,pets,pet_photos are deleted

    template_name = 'accounts/profile_delete.html'
    form_class = DeleteProfileForm
    context_object_name = 'user'
    success_url = reverse_lazy('index')

# What Does `on_delete` do in Django Models?
# https://sentry.io/answers/django-on-delete/?utm_campaign=CORP%20en%20%7C%20Auto%20%7C%20Fc%20%7C%20Corp%20V1&utm_referrer=
