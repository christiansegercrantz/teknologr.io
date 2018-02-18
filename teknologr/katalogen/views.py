from django.shortcuts import render, get_object_or_404
from members.models import *
from django.db.models import Q
from functools import reduce
from operator import and_


def _get_base_context():
    return {'abc': "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"}


def _get_consenting_persons():
    return Member.objects.filter(allow_publish_info=True)


def home(request):
    context = _get_base_context()
    context['persons'] = _get_consenting_persons()
    return render(request, 'browse.html', context)


def search(request):
    context = _get_base_context()
    query = request.GET.get('q')
    query_list = query.split()
    result = _get_consenting_persons()
    if not query_list:
        context['persons'] = []
    else:
        context['persons'] = result.filter(
           reduce(and_, (Q(given_names__icontains=q) | Q(surname__icontains=q) for q in query_list))
        )

    return render(request, 'browse.html', context)


def profile(request, member_id):
    # TODO: Check if user has permission to see profile, either public profile or own profile
    context = _get_base_context()
    person = get_object_or_404(Member, id=member_id)
    context['person'] = person
    context['functionaries'] = Functionary.objects.filter(member__id=person.id).order_by('-end_date')
    context['groups'] = GroupMembership.objects.filter(member__id=person.id).order_by('-group__end_date')
    context['decorations'] = DecorationOwnership.objects.filter(member__id=person.id).order_by('acquired')
    return render(request, 'profile.html', context)


def startswith(request, letter):
    context = _get_base_context()
    persons = _get_consenting_persons()
    context['persons'] = persons.filter(surname__istartswith=letter)
    return render(request, 'browse.html', context)
