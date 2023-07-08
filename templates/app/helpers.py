from main_app.models import Profile


def get_profile():
    profile = Profile.objects.first()
    if profile:
        return profile


# instead of using every field attrs - inherit form-control via Mixin
class BootstrapFormControlMixin:
    fields = {}

    # {'name': django.forms.fields.CharField object}
    #    K   : field
    def _init__bootstrap_form_control(self):
        for K, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class DisabledFieldsFormMixin:
    disabled_fields = ()
    fields = {}

    def _init_disabled_fields(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['readonly'] = 'readonly'
