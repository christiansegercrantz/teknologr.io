from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from members.programmes import DEGREE_PROGRAMME_CHOICES
from registration.forms import RegistrationForm
from registration.mailutils import mailApplicantSubmission


class BaseView(View):
    context = {'DEBUG': settings.DEBUG}


class HomeView(BaseView):
    template = 'registration.html'

    def get(self, request):
        self.context['programmes'] = DEGREE_PROGRAMME_CHOICES
        self.context['form'] = RegistrationForm()
        return render(request, self.template, self.context)


class SubmitView(BaseView):
    def get(self, request, **kwargs):
        previous_context = request.session.pop('context', None)
        if not previous_context:
            return redirect('registration:home')

        return render(request, 'submit.html', previous_context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.instance

            next_context = {
                'name': registration.preferred_name or registration.given_names.split()[0],
                'email': registration.email,
            }

            # FIXME: handle situation where email is not sent (e.g. admin log tool)
            try:
                mailApplicantSubmission(next_context)
            except:
                pass

            registration.save()

            request.session['context'] = next_context
            return redirect('registration:submit')
        else:
            self.context['form'] = form
            return render(request, HomeView.template, self.context, status=400)
