from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from members.models import *
from django.db.models import Q, Count
from functools import reduce
from operator import and_


def _get_base_context():
    return {'abc': "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"}


def _get_consenting_persons():
    return Member.objects.filter(allow_publish_info=True).filter(dead=False)


def _filter_valid_members(member_query):
    return [x for x in member_query if x.isValidMember()]


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
        query = result.filter(
           reduce(and_, (Q(given_names__icontains=q) | Q(surname__icontains=q) for q in query_list))
        ).order_by('surname')
        context['persons'] = _filter_valid_members(query)

    return render(request, 'browse.html', context)


@login_required
def profile(request, member_id):
    context = _get_base_context()
    person = get_object_or_404(Member, id=member_id)

    # User may view consenting profiles or their own
    # NOTE: there is a small security risk here if the members database is not in sync with the LDAP database
    if ((person.allow_publish_info and person.isValidMember() and not person.dead) or
            person.username == request.user.username):
        context['person'] = person
        context['functionaries'] = Functionary.objects.filter(member__id=person.id).order_by('-end_date')
        context['group_memberships'] = GroupMembership.objects.filter(member__id=person.id).order_by('-group__end_date')
        context['decoration_ownerships'] = DecorationOwnership.objects.filter(member__id=person.id).order_by('acquired')
        context['phux_year'] = person.getPhuxYear()
        return render(request, 'profile.html', context)
    else:
        raise PermissionDenied


@login_required
def startswith(request, letter):
    context = _get_base_context()
    persons = _get_consenting_persons().filter(surname__istartswith=letter).order_by('surname')
    context['persons'] = _filter_valid_members(persons)

    return render(request, 'browse.html', context)


@login_required
def myprofile(request):
    person = get_object_or_404(Member,  username=request.user.username)
    return redirect('katalogen.views.profile', person.id)

@login_required
def decorations(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'decorations.html', {
        'decorations': Decoration.objects.order_by('name').annotate(num_owners=Count('ownerships'))
    })

@login_required
def decoration_ownerships(request, decoration_id):
    decoration = get_object_or_404(Decoration,  id=decoration_id)

    return render(request, 'decoration_ownerships.html', {
        'decoration': decoration,
        'decoration_ownerships': DecorationOwnership.objects.filter(decoration_id=decoration_id).order_by('acquired'),
    })

@login_required
def functionary_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'functionary_types.html', {
        'functionary_types': FunctionaryType.objects.order_by('name').annotate(num_functionaries=Count('functionaries')),
    })

@login_required
def functionaries(request, functionary_type_id):
    functionary_type = get_object_or_404(FunctionaryType, id=functionary_type_id)

    return render(request, 'functionaries.html', {
        'functionary_type': functionary_type,
        'functionaries': Functionary.objects.filter(functionarytype=functionary_type_id).order_by('-end_date'),
    })

@login_required
def group_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'group_types.html', {
        'group_types': GroupType.objects.order_by('name').annotate(num_groups=Count('groups')),
    })

@login_required
def groups(request, group_type_id):
    group_type = get_object_or_404(GroupType, id=group_type_id)
    groups = group_type.groups.annotate(num_members=Count('memberships'))

    return render(request, 'groups.html', {
        'group_type': group_type,
        'groups': groups,
    })
