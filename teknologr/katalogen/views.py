from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from members.models import *
from katalogen.utils import *
from django.db.models import Q, Count
from functools import reduce
from operator import and_


def _get_base_context(request):
    return {
        'abc': "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ",
        'is_staff': request.user.is_staff if request else False,
    }


@login_required
def home(request):
    context = _get_base_context(request)
    context['home'] = True
    return render(request, 'browse.html', context)


@login_required
def search(request):
    query_list = request.GET.get('q').split()
    result = []

    if query_list:
        result = Member.objects.filter(
           reduce(and_, (Q(given_names__icontains=q) | Q(surname__icontains=q) for q in query_list))
        ).order_by('surname')

    return render(request, 'browse.html', {
        **_get_base_context(request),
        'persons': result,
    })


@login_required
def profile(request, member_id):
    person = get_object_or_404(Member, id=member_id)

    functionaries = Functionary.objects.filter(member__id=person.id).order_by('functionarytype__name', 'begin_date')
    functionary_duration_strings = create_functionary_duration_strings(functionaries)

    group_memberships = GroupMembership.objects.filter(member__id=person.id).order_by('group__grouptype__name', 'group__begin_date')
    group_type_duration_strings = create_group_type_duration_strings(group_memberships)

    return render(request, 'profile.html', {
        **_get_base_context(request),
        'show_all': person.username == request.user.username or person.showContactInformation(),
        'person': person,
        'functionary_duration_strings': functionary_duration_strings,
        'group_type_duration_strings': group_type_duration_strings,
        'decoration_ownerships': DecorationOwnership.objects.filter(member__id=person.id).order_by('acquired'),
    })


@login_required
def startswith(request, letter):
    return render(request, 'browse.html', {
        **_get_base_context(request),
        'persons': Member.objects.filter(surname__istartswith=letter).order_by('surname'),
    })


@login_required
def myprofile(request):
    person = get_object_or_404(Member,  username=request.user.username)
    return redirect('katalogen:profile', person.id)


@login_required
def decorations(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'decorations.html', {
        **_get_base_context(request),
        'decorations': Decoration.objects.order_by('name').annotate(num_owners=Count('ownerships'))
    })


@login_required
def decoration_ownerships(request, decoration_id):
    decoration = get_object_or_404(Decoration,  id=decoration_id)

    return render(request, 'decoration_ownerships.html', {
        **_get_base_context(request),
        'decoration': decoration,
        'decoration_ownerships': DecorationOwnership.objects.filter(decoration_id=decoration_id).order_by('acquired'),
    })


@login_required
def functionary_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'functionary_types.html', {
        **_get_base_context(request),
        'functionary_types': FunctionaryType.objects.order_by('name').annotate(num_functionaries=Count('functionaries')),
    })


@login_required
def functionaries(request, functionary_type_id):
    functionary_type = get_object_or_404(FunctionaryType, id=functionary_type_id)

    functionaries = functionary_type.functionaries.order_by('-end_date', 'member__surname')
    for f in functionaries:
        f.duration_string = create_duration_string(f.begin_date, f.end_date)

    return render(request, 'functionaries.html', {
        **_get_base_context(request),
        'functionary_type': functionary_type,
        'functionaries': functionaries,
    })


@login_required
def group_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'group_types.html', {
        **_get_base_context(request),
        'group_types': GroupType.objects.order_by('name').annotate(num_groups=Count('groups')),
    })


@login_required
def groups(request, group_type_id):
    group_type = get_object_or_404(GroupType, id=group_type_id)

    groups = group_type.groups.annotate(num_members=Count('memberships')).order_by('-end_date')
    for g in groups:
        g.duration_string = create_duration_string(g.begin_date, g.end_date)

    return render(request, 'groups.html', {
        **_get_base_context(request),
        'group_type': group_type,
        'groups': groups,
    })
