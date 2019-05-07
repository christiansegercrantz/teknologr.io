from django import forms
from registration.models import LimboMember
from registration.labels import MEMBERSHIP_FORM_LABELS
from members.programmes import DEGREE_PROGRAMME_CHOICES


_BOOTSTRAP_CLASS = 'form-control'
_BOOTSTRAP_RADIO_CLASS = 'form-check-input'
_EMAIL_PLACEHOLDER = '@aalto.fi'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = LimboMember
        fields = '__all__'
        labels = MEMBERSHIP_FORM_LABELS

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self._set_programme_choices()
        self._set_attributes()
        # Specify unrequired fields
        self.fields['preferred_name'].required = False

    def _set_attributes(self):
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = _BOOTSTRAP_CLASS
            f.widget.attrs['autocomplete'] = 'off'
            if type(f.widget) == forms.widgets.CheckboxInput:
                f.widget.attrs['class'] = _BOOTSTRAP_RADIO_CLASS
            if type(f.widget) == forms.widgets.Select:
                f.widget.attrs['class'] = 'form-control es-input'

        self.fields['email'].widget.attrs['placeholder'] = _EMAIL_PLACEHOLDER

    def _set_programme_choices(self):
        degree_programme_label = MEMBERSHIP_FORM_LABELS['degree_programme_options']

        programmes = [('', 'SKOLA - LINJE')]  # Default setting
        programmes.extend([
                ('{}_{}'.format(school, programme), '{} - {}'.format(school, programme))
                for school, programmes in DEGREE_PROGRAMME_CHOICES.items()
                for programme in programmes
        ])
        programmes.append(('extra', 'ÖVRIG'))

        self.fields['degree_programme_options'] = forms.ChoiceField(
                choices=programmes,
                label=degree_programme_label,
                widget=forms.widgets.Select(attrs={'id': 'id_degree_programme_options'}))

        self.fields['degree_programme'] = forms.CharField(
                label=MEMBERSHIP_FORM_LABELS['degree_programme'],
                widget=forms.widgets.TextInput(attrs={'placeholder': degree_programme_label}))
