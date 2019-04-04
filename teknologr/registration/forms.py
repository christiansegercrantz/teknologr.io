from django import forms
from registration.models import LimboMember
from registration.labels import MEMBERSHIP_FORM_LABELS


BOOTSTRAP_CLASS = 'form-control'
BOOTSTRAP_RADIO_CLASS = 'form-check-input'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = LimboMember
        fields = '__all__'
        labels = MEMBERSHIP_FORM_LABELS

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = BOOTSTRAP_CLASS
            if type(f.widget) == forms.widgets.CheckboxInput:
                f.widget.attrs['class'] = BOOTSTRAP_RADIO_CLASS

        self.fields['email'].widget.attrs['placeholder'] = '@aalto.fi'
