from members.models import *
from registration.models import Applicant
from django.forms import ModelForm, DateField, ChoiceField, CharField
from django.forms.widgets import CheckboxInput, DateInput, HiddenInput, TextInput, PasswordInput
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class BSModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BSModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if type(field.widget) is CheckboxInput:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
    birth_date = DateField(widget=DateInput(attrs={'type': 'date'}), required=False)


class GroupTypeForm(BSModelForm):
    class Meta:
        model = GroupType
        fields = '__all__'


class FunctionaryTypeForm(BSModelForm):
    class Meta:
        model = FunctionaryType
        fields = '__all__'


class FunctionaryForm(BSModelForm):
    class Meta:
        model = Functionary
        fields = '__all__'

    member = AutoCompleteSelectField('member', required=True, help_text=None)
    begin_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = DateField(widget=DateInput(attrs={'type': 'date'}))


class DecorationForm(BSModelForm):
    class Meta:
        model = Decoration
        fields = '__all__'


class DecorationOwnershipForm(BSModelForm):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'

    acquired = DateField(widget=DateInput(attrs={'type': 'date'}))
    member = AutoCompleteSelectField('member', required=True, help_text=None)


class GroupForm(BSModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    begin_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = DateField(widget=DateInput(attrs={'type': 'date'}))


class GroupMembershipForm(BSModelForm):

    class Meta:
        model = GroupMembership
        fields = '__all__'

    # member = AutoCompleteSelectField('member', required=True, help_text=None)
    member = AutoCompleteSelectMultipleField('member', required=True, help_text=None)


class MemberTypeForm(BSModelForm):
    class Meta:
        model = MemberType
        fields = '__all__'

    begin_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = DateField(required=False, widget=DateInput(attrs={'type': 'date'}))


class BSAuthForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Användarnamn', 'autofocus': 'on'
    }))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Lösenord'}))


class ApplicantAdditionForm(BSModelForm):
    class Meta:
        model = Applicant
        fields = '__all__'

    membership_date = DateField(widget=DateInput(attrs={'type': 'date'}))
    phux_date = DateField(widget=DateInput(attrs={'type': 'date'}), required=False)


class MultipleApplicantAdditionForm(ApplicantAdditionForm):
    applicant = AutoCompleteSelectMultipleField('applicant', required=True, help_text=None)
