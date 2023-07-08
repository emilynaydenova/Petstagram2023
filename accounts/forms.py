from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import Profile
from common.helpers import BootstrapFormControlMixin


# instead of forms.ModelForm -> UserCreationForm + fields from Profile
class CreateProfileForm(BootstrapFormControlMixin, UserCreationForm):
    # fields from BaseUserCreationForm (username,password...)

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        label="First Name:",
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        label="Last Name:",
    )
    pictureURL = forms.URLField(
        required=False,
        label="Link to URL picture:",
    )
    DoB = forms.DateField(required=False, label="Date of Birth:", )
    description = forms.CharField(
        widget=forms.Textarea(),
        required=False,

    )
    email = forms.EmailField(required=False, )
    gender = forms.ChoiceField(choices=Profile.GENDERS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()

    def save(self, commit=True):
        user = super().save(commit=False)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            pictureURL=self.cleaned_data['pictureURL'],
            DoB=self.cleaned_data['DoB'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],

            user=user,
        )
        if commit:
            user.save()
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'pictureURL',
                  'description', 'email', 'gender']

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    #       'class': 'form-control',
                    'placeholder': 'Enter first name'
                }),
            "last_name": forms.TextInput(
                attrs={
                    #        'class': 'form-control',
                    'placeholder': 'Enter last name'
                }),
            "pictureURL": forms.URLInput(
                attrs={
                    #        'class': 'form-control',
                    'placeholder': 'Enter URL'
                }),

        }

# !!!!!! Default choice value
class EditProfileForm(BootstrapFormControlMixin,forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init__bootstrap_form_control()
    #     # assign a (computed, I assume) default value to the choice field
    #     self.initial['gender'] = Profile.DO_NOT_SHOW

    def clean_DoB(self):
        DoB = self.cleaned_data['DoB']
        if DoB:
            begin_date = date(1920, 1, 1)
            end_date = date.today()
            if DoB < begin_date or DoB > end_date:
                raise ValidationError(f"Date must be between {begin_date} and {end_date}today.")
        return DoB

    class Meta:
        model = Profile
        # fields = CreateProfileForm.Meta.fields
        # fields.extend(['DoB', 'email', 'gender', 'description'])
        fields = ['first_name', 'last_name', 'pictureURL',
                  'description', 'email', 'gender','DoB']


        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    #       'class': 'form-control',
                    'placeholder': 'Enter first name'
                }),
            "last_name": forms.TextInput(
                attrs={
                    #        'class': 'form-control',
                    'placeholder': 'Enter last name'
                }),
            "picture": forms.URLInput(
                attrs={
                    #        'class': 'form-control',
                    'placeholder': 'Enter URL'
                }),
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if "date_of_birth" : forms.DateField(....) use clean_date_of_birth() to validate year
            "DoB": forms.SelectDateWidget(
                attrs={
                    'placeholder': 'Date of birth',

                },
                years=[x for x in range(1920, (date.today().year + 1))],
            ),
            "email": forms.EmailInput(
                attrs={'placeholder': 'Enter email'},
            ),

            #   "gender":  forms.Select(choices=GENDERS,initial=GENDERS.DO_NOT_SHOW),

            "description": forms.Textarea(
                attrs={'placeholder': 'Enter description',
                       'rows': 3},
            )}

        # required_fields_except = ['date_of_birth', 'email', 'gender', 'description']


#     default_data = {'gender': Profile.DO_NOT_SHOW, } -> in model

class DeleteProfileForm(forms.ModelForm):
    # def save(self, commit=True):
    #     # should be done with signals
    #     # because this breaks the abstraction of the auth of app
    #     pets = list(self.instance.pet_set.all())
    #     PetPhoto.objects.filter(tagged_pets__in=pets).delete()
    #     self.instance.delete()
    #     return self.instance

    class Meta:
        model = get_user_model()
        fields = ()
