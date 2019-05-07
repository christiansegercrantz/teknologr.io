from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from members.programmes import DEGREE_PROGRAMME_CHOICES
from registration.forms import RegistrationForm


def _get_base_context():
    return {'DEBUG': settings.DEBUG}


def home(request):
    context = _get_base_context()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/registration/')
    else:
        context['programmes'] = DEGREE_PROGRAMME_CHOICES
        context['form'] = RegistrationForm()

    return render(request, 'registration.html', context)


def submit(request):
    pass
