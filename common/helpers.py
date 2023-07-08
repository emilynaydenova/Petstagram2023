from app.models import Profile


# instead of using every field attrs - inherit form-control via Mixin
class BootstrapFormControlMixin:
    fields = {}

    # {'name': django.forms.fields.CharField object}
    #    field_name   : field_value
    def _init__bootstrap_form_control(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class DisabledFieldsFormMixin:
    fields = '__all__'

    # !!!! - disabled + notrequired !!!!
    def _init_disabled_fields(self):
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = True
            field.required = False
