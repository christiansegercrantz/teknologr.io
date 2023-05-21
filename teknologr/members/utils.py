import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from .models import *
from locale import strxfrm

def getCurrentDate():
    return datetime.datetime.now()


def getCurrentYear():
    return getCurrentDate().year


def getFirstDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 1, 1)


def getLastDayOfCurrentYear():
    return datetime.date(getCurrentYear(), 12, 31)

def get_member_prefetched(member_id):
    '''
    This is done in 5 queries:
      1. SELECT Member WHERE id=member_id
      2. SELECT DecorationOwnership WHERE member__id=member_id
      3. SELECT Functionary WHERE member__id=member_id
      4. SELECT GroupMembership WHERE member__id=member_id
      5. SELECT MemberType WHERE member__id=member_id
    '''
    queryset = Member.objects.prefetch_related(
        Prefetch('decoration_ownerships', queryset=DecorationOwnership.objects.select_related('decoration')),
        Prefetch('functionaries', queryset=Functionary.objects.select_related('functionarytype')),
        Prefetch('group_memberships', queryset=GroupMembership.objects.select_related('group', 'group__grouptype')),
        'member_types',
    )
    return get_object_or_404(queryset, id=member_id)

def get_decorations_ordered_and_annotated():
    decorations = Decoration.objects.annotate(count=Count('ownerships'))

    # Sort manually to get a suitable order that respects ÅÄÖ but not lower/upper cases
    decorations = list(decorations)
    decorations.sort(key=lambda d: strxfrm(d.name))
    return decorations

def get_decoration_prefetched(decoration_id):
    '''
    This is done in 2 queries:
      1. SELECT Decoration WHERE id=decoration_id
      2. SELECT DecorationOwnership WHERE decoration__id=decoration_id
    '''
    queryset = Decoration.objects.prefetch_related(
        Prefetch('ownerships', queryset=DecorationOwnership.objects.select_related('member')),
    )
    return get_object_or_404(queryset, id=decoration_id)

def get_functionary_types_ordered_and_annotated():
    functionary_types = FunctionaryType.objects.annotate(
        count=Count('functionaries'),
        count_unique=Count('functionaries__member', distinct=True)
    )

    # Sort manually to get a suitable order that respects ÅÄÖ but not lower/upper cases
    functionary_types = list(functionary_types)
    functionary_types.sort(key=lambda ft: strxfrm(ft.name))
    return functionary_types

def get_functionary_type_prefetched(functionary_type_id):
    '''
    This is done in 2 queries:
      1. SELECT FunctionaryType WHERE id=functionary_type_id
      2. SELECT Functionary WHERE functionarytype__id=functionary_type_id
    '''
    queryset = FunctionaryType.objects.prefetch_related(
        Prefetch('functionaries', queryset=Functionary.objects.select_related('member')),
    )
    return get_object_or_404(queryset, id=functionary_type_id)

def get_group_types_ordered_and_annotated():
    group_types = GroupType.objects.annotate(
        count=Count('groups', distinct=True),
        count_non_empty=Count('groups', distinct=True, filter=Q(groups__memberships__gt=0)),
        count_members_total=Count('groups__memberships'),
        count_members_unique=Count('groups__memberships__member', distinct=True)
    )

    # Sort manually to get a suitable order that respects ÅÄÖ but not lower/upper cases
    group_types = list(group_types)
    group_types.sort(key=lambda gt: strxfrm(gt.name))
    return group_types

def get_group_type_prefetched(group_type_id):
    '''
    This is done in 3 queries:
      1. SELECT GroupType WHERE id=group_type_id
      2. SELECT Group WHERE grouptype__id=group_type_id
      3. SELECT GroupMembership WHERE group__id IN ^
    '''
    queryset = GroupType.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.annotate(num_members=Count('memberships', distinct=True))),
        Prefetch('groups__memberships', queryset=GroupMembership.objects.select_related('member')),
    )
    return get_object_or_404(queryset, id=group_type_id)
