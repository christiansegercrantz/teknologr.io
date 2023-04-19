from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncYear
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
        ).order_by('surname', 'given_names')

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
        'persons': Member.objects.filter(surname__istartswith=letter).order_by('surname', 'given_names'),
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
def decoration(request, decoration_id):
    decoration = get_object_or_404(Decoration,  id=decoration_id)

    return render(request, 'decoration_ownerships.html', {
        **_get_base_context(request),
        'decoration': decoration,
        'decoration_ownerships': DecorationOwnership.objects.filter(decoration_id=decoration_id).order_by('-acquired', 'member__surname', 'member__given_names'),
    })


@login_required
def functionary_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'functionary_types.html', {
        **_get_base_context(request),
        'functionary_types': FunctionaryType.objects.order_by('name').annotate(num_total=Count('functionaries'), num_unique=Count('functionaries__member__id', distinct=True)),
    })


@login_required
def functionary_type(request, functionary_type_id):
    functionary_type = get_object_or_404(FunctionaryType, id=functionary_type_id)

    functionaries = functionary_type.functionaries.order_by('-end_date', 'member__surname', 'member__given_names')
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
        'group_types': GroupType.objects.annotate(num_groups=Count('groups', distinct=True, filter=Q(groups__memberships__gt=0)), num_members_total=Count('groups__memberships__member__id'), num_members_unique=Count('groups__memberships__member__id', distinct=True)).order_by('name'),
    })


@login_required
def group_type(request, group_type_id):
    group_type = get_object_or_404(GroupType, id=group_type_id)

    groups = group_type.groups.annotate(num_members=Count('memberships', distinct=True)).filter(num_members__gt=0).order_by('-end_date')
    for g in groups:
        g.duration_string = create_duration_string(g.begin_date, g.end_date)
        # XXX: Is there a better way to order the memberships in group?
        g.memberships_ordered = g.memberships.order_by('member__surname', 'member__given_names')

    return render(request, 'groups.html', {
        **_get_base_context(request),
        'group_type': group_type,
        'groups': groups,
    })


@login_required
def years(request):
    years = {}

    def add(obj, key, count_key=None):
        date = obj['year']
        if date == None:
            return

        y = date.year
        if y not in years:
            years[y] = {}
        years[y][key] = obj[count_key or key]

    # Get all functionaries and group them by their start year, and for each year return a count for the total amount of functionaries and the amount of unique members holding the posts
    f_counts = Functionary.objects.annotate(year=TruncYear('begin_date')).values('year').annotate(functionaries_total=Count('id'), functionaries_unique=Count('member__id', distinct=True)).values('year', 'functionaries_total', 'functionaries_unique')
    for obj in f_counts:
        add(obj, 'functionaries_total')
        add(obj, 'functionaries_unique')

    # Get groups and group them by their start year, and for each year return a count for the total amount of groups, the total amount of members in the groups, and the amount of unique members holding in the groups
    gm_counts = GroupMembership.objects.annotate(year=TruncYear('group__begin_date')).values('year').annotate(groups=Count('group', distinct=True), group_memberships_total=Count('member'), group_memberships_unique=Count('member', distinct=True)).values('year', 'groups', 'group_memberships_total', 'group_memberships_unique')
    for obj in gm_counts:
        add(obj, 'groups')
        add(obj, 'group_memberships_total')
        add(obj, 'group_memberships_unique')

    # Get all decorations and group them by the year they were aquired, and return a count for each year
    do_counts = DecorationOwnership.objects.annotate(year=TruncYear('acquired')).values('year').annotate(decoration_ownerships=Count('id')).values('year', 'decoration_ownerships')
    for obj in do_counts:
        add(obj, 'decoration_ownerships')

    # Get all StÄlMs and ordinary members and group them by the year they became members, and return a count for each type/year combination
    m_counts = MemberType.objects.filter(Q(type='OM') | Q(type='ST')).annotate(year=TruncYear('begin_date')).values('year', 'type').annotate(members=Count('member')).values('year', 'type', 'members')
    for obj in m_counts:
        add(obj, 'members_ordinary' if obj['type'] == 'OM' else 'members_stalm', 'members')

    return render(request, 'years.html', {
        **_get_base_context(request),
        'years': dict(sorted(years.items(), reverse=True)),
    })

@login_required
def year(request, year):
    # Get all decoration ownerships for the year
    decoration_ownerships = DecorationOwnership.objects.annotate(year=TruncYear('acquired')).filter(year=f'{year}-01-01').order_by('decoration__name', 'member__surname', 'member__given_names')

    # Get all functionaries for the year
    functionaries = Functionary.objects.annotate(year=TruncYear('begin_date')).filter(year=f'{year}-01-01').order_by('functionarytype__name', 'member__surname', 'member__given_names')

    # Get all groups for the year
    groups = Group.objects.annotate(year=TruncYear('begin_date')).filter(year=f'{year}-01-01').annotate(num_members=Count('memberships', distinct=True)).filter(num_members__gt=0).order_by('grouptype__name')
    for g in groups:
        # XXX: Is there a better way of sorting the memberships?
        g.memberships_ordered = g.memberships.order_by('member__surname', 'member__given_names')

    # Count the number of total and unique group memebers
    gm_counts = groups.aggregate(total=Count('memberships__member__id'), unique=Count('memberships__member__id', distinct=True))

    # Get all new members for the year
    member_types = MemberType.objects.annotate(year=TruncYear('begin_date')).filter(year=f'{year}-01-01').order_by('member__surname', 'member__given_names')

    return render(request, 'year.html', {
        **_get_base_context(request),
        'year': year,
        'decoration_ownerships': decoration_ownerships,
        'functionaries': functionaries,
        'functionaries_unique_count': functionaries.aggregate(count=Count('member__id', distinct=True))['count'],
        'groups': groups,
        'group_memberships_total': gm_counts['total'],
        'group_memberships_unique': gm_counts['unique'],
        'member_types_ordinary': member_types.filter(type='OM'),
        'member_types_stalm': member_types.filter(type='ST'),
    })
