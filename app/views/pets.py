from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from app.forms import CreatePetForm, EditPetForm, DeletePetForm
from app.models import Pet


class CreatePetView(CreateView):
    template_name = 'app/pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('dashboard')

    # give 'user' as kwargs to CreatePetForm
    def get_form_kwargs(self): # from ModelFormMixin
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

"""
    # to check for valid user ->
    # - override form_valid
    # - or add user_id to the form and make save()
    def form_valid(self, form):
        u = self.request.user
        # ................
        return super().form_valid(form)
"""


class EditPetView(UpdateView):
    model = Pet
    template_name = 'app/pet_edit.html'
    form_class = EditPetForm
    context_object_name = 'pet'

    def get_success_url(self):
        profile_id = self.object.user_id
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class DeletePetView(DeleteView):
    template_name = 'app/pet_delete.html'
    form_class = DeletePetForm


# def edit_pet(request, pk):
#     pet = Pet.objects.get(pk=pk)
#     if request.method == 'POST':
#         pet_form = EditPetForm(request.POST, instance=pet)
#         # put data from request.POST on instance ~ PUT
#         if pet_form.is_valid():
#             pet_form.save()
#             return redirect('profile details')
#     else:
#
#         pet_form = EditPetForm(instance=pet)  # populate the form with the record
#
#     context = {
#         'pet': pet,
#         'pet_form': pet_form,
#     }
#     return render(request, "main/pet_edit.html",context)