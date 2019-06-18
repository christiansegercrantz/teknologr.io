# -*- coding: utf-8 -*-

from django.db.models import Q
from members.models import Member
from registration.models import Applicant
from datetime import date


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
