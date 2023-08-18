# -*- coding: utf-8 -*-

from django.db.models import Q
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.pagination import LimitOffsetPagination
from members.models import Member
from registration.models import Applicant
from datetime import datetime
from rest_framework.response import Response

def findMembers(query, count=50):
    members = Member.objects.search_by_name(query.split(), True)[:count]
    Member.order_by(members, 'name')
    return members

def findApplicants(query, count=50):
    args = []

    for word in query.split():
        args.append(Q(given_names__icontains=word) | Q(surname__icontains=word))

    if not args:
        return []

    return Applicant.objects.filter(*args).order_by('surname', 'given_names')[:count]


def create_dump_response(content, name, filetype):
    dumpname = f'filename="{name}_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.{filetype}'
    return Response(
        content,
        status=200,
        headers={'Content-Disposition': f'attachment; {dumpname}'}
    )

def assert_public_member_fields(fields):
    assert len(set(fields).intersection(set(Member.STAFF_ONLY_FIELDS + Member.HIDABLE_FIELDS))) == 0, 'Only 100% public Member fields allowed'


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


class Pagination(LimitOffsetPagination):
    default_limit = 100
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000
