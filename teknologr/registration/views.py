from django.shortcuts import render
from members.programmes import DEGREE_PROGRAMME_CHOICES


def home(request):
    context = {'programmes': DEGREE_PROGRAMME_CHOICES}
    return render(request, 'registration.html', context)

