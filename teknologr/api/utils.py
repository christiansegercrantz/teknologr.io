# -*- coding: utf-8 -*-

from django.db.models import Q
from rest_framework.renderers import BrowsableAPIRenderer
from members.models import Member
from registration.models import Applicant


def findMembers(query, count=50):

    args = []

    for word in query.split():
        args.append(Q(given_names__icontains=word) | Q(surname__icontains=word))

    if not args:
        return []  # No words in query (only spaces?)

    return Member.objects.filter(*args).order_by('surname', 'given_names')[:count]


def findApplicants(query, count=50):
    args = []

    for word in query.split():
        args.append(Q(given_names__icontains=word) | Q(surname__icontains=word))

    if not args:
        return []

    return Applicant.objects.filter(*args).order_by('surname', 'given_names')[:count]

class BrowsableAPIRendererWithoutForms(BrowsableAPIRenderer):
    """ Custom renderer for the browsable API that hides the form. """

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx['display_edit_forms'] = False
        return ctx

    def show_form_for_method(self, view, method, request, obj):
        return False

    def get_rendered_html_form(self, data, view, method, request):
        return ''
