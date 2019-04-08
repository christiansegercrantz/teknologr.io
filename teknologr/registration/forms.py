from django import forms
from registration.models import LimboMember
from registration.labels import MEMBERSHIP_FORM_LABELS
from members.programmes import DEGREE_PROGRAMME_CHOICES


BOOTSTRAP_CLASS = 'form-control'
BOOTSTRAP_RADIO_CLASS = 'form-check-input'
EMAIL_PLACEHOLDER = '@aalto.fi'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = LimboMember
        fields = '__all__'
        labels = MEMBERSHIP_FORM_LABELS

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self._set_programme_choices()
        self._set_attributes()

    def _set_attributes(self):
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = BOOTSTRAP_CLASS
            f.widget.attrs['autocomplete'] = 'off'
            if type(f.widget) == forms.widgets.CheckboxInput:
                f.widget.attrs['class'] = BOOTSTRAP_RADIO_CLASS
            if type(f.widget) == forms.widgets.Select:
                f.widget.attrs['class'] = 'form-control es-input'

        self.fields['email'].widget.attrs['placeholder'] = EMAIL_PLACEHOLDER

    def _set_programme_choices(self):
        programmes = [('', 'SKOLA - LINJE')]  # Default setting
        programmes.extend([
                ('{}_{}'.format(school, programme), '{} - {}'.format(school, programme))
                for school, programmes in DEGREE_PROGRAMME_CHOICES.items()
                for programme in programmes
        ])
        self.fields['degree_programme'] = forms.ChoiceField(
                choices=programmes,
                required=True,
                label=MEMBERSHIP_FORM_LABELS['degree_programme'])
