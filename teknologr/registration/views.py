from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from members.programmes import DEGREE_PROGRAMME_CHOICES
from registration.forms import RegistrationForm
from registration.models import LimboMember


class BaseView(View):
    context = {'DEBUG': settings.DEBUG}


class HomeView(BaseView):
    template = 'registration.html'

    def get(self, request):
        self.context['programmes'] = DEGREE_PROGRAMME_CHOICES
        self.context['form'] = RegistrationForm()
        return render(request, self.template, self.context)


class SubmitView(BaseView):
    template = 'submit.view'

    """
    def get(self, request):
        applicant = LimboMember()
    """

    def post(self, request):
        # TODO: add context
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.instance
            registration.save()
        else:
            self.context['form'] = form
            return render(request, 'registration.html', self.context, status=400)

        render(request, 'submit.html')
