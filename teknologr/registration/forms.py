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
        self._set_attributes()
        self._set_programme_choices()

    def _set_attributes(self):
        for fname, f in self.fields.items():
            f.widget.attrs['class'] = BOOTSTRAP_CLASS
            if type(f.widget) == forms.widgets.CheckboxInput:
                f.widget.attrs['class'] = BOOTSTRAP_RADIO_CLASS

        self.fields['email'].widget.attrs['placeholder'] = EMAIL_PLACEHOLDER

    def _set_programme_choices(self):
        schools = [(school, school) for school in DEGREE_PROGRAMME_CHOICES.keys()]
        self.fields['school'] = forms.ChoiceField(choices=schools, required=True)

        # FIXME: set these as hidden options, shown only when the school above is chosen
        programme_options = [
            forms.ChoiceField(choices=enumerate(programmes))
            for school, programmes
            in DEGREE_PROGRAMME_CHOICES.items()
        ]
