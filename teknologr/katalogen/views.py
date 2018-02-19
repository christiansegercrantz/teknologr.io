from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from members.models import *
from django.db.models import Q
from functools import reduce
from operator import and_


def _get_base_context():
    return {'abc': "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"}


def _get_consenting_persons():
    return Member.objects.filter(allow_publish_info=True)


@login_required
def home(request):
    context = _get_base_context()
    context['home'] = True
    return render(request, 'browse.html', context)


@login_required
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
        ).order_by('surname')

    return render(request, 'browse.html', context)


@login_required
def profile(request, member_id):
    context = _get_base_context()
    person = get_object_or_404(Member, id=member_id)

    # User may view consenting profiles or their own
    # NOTE: there is a small security risk here if the members database is not in sync with the LDAP database
    if person.allow_publish_info or person.username == request.user.username:
        context['person'] = person
        context['functionaries'] = Functionary.objects.filter(member__id=person.id).order_by('-end_date')
        context['groups'] = GroupMembership.objects.filter(member__id=person.id).order_by('-group__end_date')
        context['decorations'] = DecorationOwnership.objects.filter(member__id=person.id).order_by('acquired')
        return render(request, 'profile.html', context)
    else:
        return HttpResponseForbidden()


@login_required
def startswith(request, letter):
    context = _get_base_context()
    persons = _get_consenting_persons()
    context['persons'] = persons.filter(surname__istartswith=letter).order_by('surname')
    return render(request, 'browse.html', context)


@login_required
def myprofile(request):
    person = get_object_or_404(Member,  username=request.user.username)
    return redirect('katalogen.views.profile', person.id)
