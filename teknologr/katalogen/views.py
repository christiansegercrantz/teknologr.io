from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncYear
from members.models import *
from members.utils import *
from katalogen.utils import *
from django.db.models import Q, Count, Prefetch
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
    person = get_member_prefetched_and_ordered(member_id)

    functionary_duration_strings = create_functionary_duration_strings(person.functionaries.all())
    group_type_duration_strings = create_group_type_duration_strings(person.group_memberships.all())

    return render(request, 'profile.html', {
        **_get_base_context(request),
        'show_all': person.username == request.user.username or person.showContactInformation(),
        'person': person,
        'functionary_duration_strings': functionary_duration_strings,
        'group_type_duration_strings': group_type_duration_strings,
        'decoration_ownerships': person.decoration_ownerships.all(),
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
        'decorations': get_decorations_ordered_and_annotated()
    })


@login_required
def decoration(request, decoration_id):
    decoration = get_decoration_prefetched_and_ordered(decoration_id)
    decoration_ownerships = decoration.ownerships.all()

    return render(request, 'decoration_ownerships.html', {
        **_get_base_context(request),
        'decoration': decoration,
        'decoration_ownerships': decoration_ownerships,
    })


@login_required
def functionary_types(request):
    # XXX: More info:
    #  - Date of first/latest?
    return render(request, 'functionary_types.html', {
        **_get_base_context(request),
        'functionary_types': get_functionary_types_ordered_and_annotated(),
    })


@login_required
def functionary_type(request, functionary_type_id):
    functionary_type = get_functionary_type_prefetched_and_ordered(functionary_type_id)
    functionaries = functionary_type.functionaries.all()

    # Add date interval string to all functionaries
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
        'group_types': get_group_types_ordered_and_annotated(),
    })


@login_required
def group_type(request, group_type_id):
    group_type = get_group_type_prefetched_and_ordered(group_type_id)

    # Do not want to display empty groups here, but filtering that in the template instead of the query
    groups = group_type.groups.all()

    # Add date interval string to all groups
    for g in groups:
        g.duration_string = create_duration_string(g.begin_date, g.end_date)

    return render(request, 'groups.html', {
        **_get_base_context(request),
        'group_type': group_type,
        'groups': groups,
    })


@login_required
def years(request):
    '''
    This is done in 4 queries, as you would expect by reading the code:
      1. SELECT Functionary => COUNT
      2. SELECT GroupMembership => COUNT
      3. SELECT DecortaionOwnership => COUNT
      4. SELECT MemberType WHERE type IN ["OM", "ST"] => COUNT
    '''
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
    # XXX: This does not include all valid date intervals
    f_counts = Functionary.objects.annotate(year=TruncYear('begin_date')).values('year').annotate(functionaries_total=Count('id'), functionaries_unique=Count('member__id', distinct=True)).values('year', 'functionaries_total', 'functionaries_unique')
    for obj in f_counts:
        add(obj, 'functionaries_total')
        add(obj, 'functionaries_unique')

    # Get groups and group them by their start year, and for each year return a count for the total amount of groups, the total amount of members in the groups, and the amount of unique members holding in the groups
    # XXX: This does not include all valid date intervals
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
    '''
    This could be enhanced, but curretnly it is done with 10 queries:
      1. SELECT DecortaionOwnership WHERE correct_year
      2. SELECT Functionary WHERE correct_year
      3. group_ids, group_type_ids = SELECT Group WHERE correct_year
      4. SELECT GroupMemebership WHERE group__id IN group_ids
      5. SELECT GroupType WHERE id IN group_type_ids
      6. SELECT MemberType WHERE correct_year AND type="OM"
      7. SELECT MemberType WHERE correct_year AND type="ST"
      8. SELECT GroupMemebership WHERE correct_year => COUNT
      9. COUNT DISTINCT over ^
      10. SELECT Functionary WHERE correct_year => COUNT
    '''
    first_day = datetime.date(int(year), 1, 1)
    last_day = datetime.date(int(year), 12, 31)

    # Get all decoration ownerships for the year
    decoration_ownerships = DecorationOwnership.objects.select_related('member', 'decoration').filter(acquired__year=year).order_by('decoration__name', 'member__surname', 'member__given_names')

    # Get all functionaries for the year
    functionaries = Functionary.objects.select_related('member', 'functionarytype').filter(begin_date__lte=last_day, end_date__gte=first_day).order_by('functionarytype__name', 'member__surname', 'member__given_names')

    # Get all groups and group memberships for the year
    groups = Group.objects.prefetch_related(
        Prefetch(
            'memberships',
            queryset=GroupMembership.objects.select_related('member').order_by('member__surname', 'member__given_names')
        ),
        'grouptype'
    ).annotate(num_members=Count('memberships', distinct=True)).filter(begin_date__lte=last_day, end_date__gte=first_day, num_members__gt=0).order_by('grouptype__name')

    # Count the number of total and unique group memebers
    gm_counts = groups.aggregate(total=Count('memberships__member__id'), unique=Count('memberships__member__id', distinct=True))

    # Get all new members for the year
    member_types = MemberType.objects.select_related('member').filter(begin_date__year=year).order_by('member__surname', 'member__given_names')

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
