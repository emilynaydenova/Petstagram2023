from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from app.forms import EditPetPhotoForm, CreatePetPhotoForm
from app.models import PetPhoto


class PetPhotoDetailsView(DetailView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
    model = PetPhoto
    template_name = 'app/photo_details.html'
    context_object_name = 'pet_photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_logged'] = self.request.user.is_authenticated
        context['is_owner'] = self.object.user == self.request.user
        # object.user from DetailView

        return context

    # to use prefetch_related
    def get_queryset(self):
        return super().get_queryset()\
            .prefetch_related('tagged_pets')\
            .order_by('created')



# -------------------------------------------------------------


# make separate table - user-photo like (unique)
def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect("pet photo details", pk)


# -------- Create Photo ----------------------------

class CreatePetPhotoView(LoginRequiredMixin, CreateView):
    model = PetPhoto
    template_name = 'app/photo_create.html'

    form_class = CreatePetPhotoForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # add 'user' to form data
        form.instance.user = self.request.user
        return super().form_valid(form)


# -----Edit Pet Photo -------------------------------------------------
class EditPetPhotoView(UpdateView):
    model = PetPhoto  # model
    # !!! without picture -> so you can't change it
    # fields = ('description', 'tagged_pets')  # fields / if you want to select all fields, use "__all__"
    form_class = EditPetPhotoForm
    template_name = 'app/photo_edit.html'  # template for updating
    context_object_name = 'pet_photo'

    def get_success_url(self):
        return reverse_lazy('pet photo details', kwargs={'pk': self.object.pk})


class DeletePetPhotoView(DeleteView):
    pass
