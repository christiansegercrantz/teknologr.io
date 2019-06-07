from django.shortcuts import render, redirect
from django.conf import settings
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
    template = 'submit.html'

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # TODO: send mail to user as affirmation (check `api/mailutils.py`)
            self.context['name'] = form.instance.preferred_name or form.instance.given_names.split(' ')[0]

            registration = form.instance
            registration.save()
        else:
            self.context['form'] = form
            return render(request, HomeView.template, self.context, status=400)

        return render(request, self.template, self.context)
