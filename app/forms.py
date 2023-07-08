from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from common.helpers import BootstrapFormControlMixin, DisabledFieldsFormMixin
from app.models import Pet, PetPhoto

"""
Field Options	Description
required	By default, each Field class assumes the value is required, so to make it not required you need to set required=False
label	The label argument lets you specify the “human-friendly” label for this field. This is used when the Field is displayed in a Form.
label_suffix	The label_suffix argument lets you override the form’s label_suffix on a per-field basis.
widget	The widget argument lets you specify a Widget class to use when rendering this Field. See Widgets for more information.
help_text	The help_text argument lets you specify descriptive text for this Field. If you provide help_text, it will be displayed next to the Field when the Field is rendered by one of the convenience Form methods.
error_messages	The error_messages argument lets you override the default messages that the field will raise. Pass in a dictionary with keys matching the error messages you want to override.
validators	The validators argument lets you provide a list of validation functions for this field.
localize	The localize argument enables the localization of form data input, as well as the rendered output.
disabled.	The disabled boolean argument, when set to True, disables a form field using the disabled HTML attribute so that it won’t be editable by users.
"""


# add user in form
class CreatePetForm(BootstrapFormControlMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init__bootstrap_form_control()

    # can redefine save() method -
    # what to do when make save() in the view for that form
    def save(self, commit=True):
        pet = super().save(commit=False)
        pet.user = self.user
        if commit:
            pet.save()
        return pet

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['DoB']
        if date_of_birth:
            begin_date = date(2000, 1, 1)
            end_date = date.today()
            if date_of_birth < begin_date or date_of_birth > end_date:
                raise ValidationError(
                    f"Date must be between {begin_date.day}.{begin_date.month}.{begin_date.year} and today.")
        return date_of_birth

    class Meta:
        model = Pet
        fields = ['name', 'type', 'DoB']
        widgets = {
            "name": forms.TextInput(
                attrs={
                    'placeholder': 'Enter pet name'
                }, ),

            "DoB": forms.SelectDateWidget(
                attrs={},
                years=[x for x in range(2000, (date.today().year + 1))],
            ),
        }
        labels = {
            "name": "Pet Name:",
            "type": 'Type:',
            "DoB": 'Day of Birth',
        }
        unique_together = {'name', 'user_profile'}


class EditPetForm(BootstrapFormControlMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = Pet
        exclude = ['user',]
        widgets = {
            "DoB": forms.SelectDateWidget(
                attrs={},

                # min-max date
                years=[x for x in range(2000, (date.today().year + 1))],
            ),
        }


class DeletePetForm(BootstrapFormControlMixin, DisabledFieldsFormMixin, forms.ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()
        self._init_disabled_fields()

    def save(self, commit=True):  # custom logic
        # what to make form when object is deleted
        self.instance.delete()
        return self.instance

    class Meta:
        model = Pet
        exclude = ('user',)


class CreatePetPhotoForm(BootstrapFormControlMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    class Meta:
        model = PetPhoto
        exclude = ['likes']
        widgets = {
            "description": forms.Textarea(
                attrs={
                    #       'class': 'form-control',
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            #  "tagged_pets": forms.Select() -> shows what is in __str__ of the model

        }
        labels = {
            "photoFile": "Pet Image:",
            "description": "Description:",
            "tagged_pets": "Tag Pets",
        }


class EditPetPhotoForm(BootstrapFormControlMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

        self.fields['photoFile'].required = False

    class Meta:
        model = PetPhoto
        exclude = ['likes','user']
        widgets = {
            # "photo": forms.TextInput(
            #      attrs = {'disabled': True,}
            #  ),
            # not allow editing but show photo
            # to show picture -> in template <img src="{{ pet_photo.photo.value.url }}"
            # "photoFile": forms.HiddenInput(),

            "description": forms.Textarea(
                attrs={
                    #       'class': 'form-control',
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            #  "tagged_pets": forms.Select() -> shows what is in __str__ of the model

        }
        labels = {
            "photoFile": '',
            "description": "Description:",
            "tagged_pets": "Tag Pets",
        }
