# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q, Prefetch, Count
from django_countries.fields import CountryField
from django.shortcuts import get_object_or_404
from locale import strxfrm, strcoll
from operator import attrgetter
from katalogen.utils import *
from members.utils import *


class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MemberManager(models.Manager):
    def get_prefetched_or_404(self, member_id):
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

class Member(SuperClass):
    objects = MemberManager()

    # NAMES
    given_names = models.CharField(max_length=64, blank=False, null=False, default="UNKNOWN")
    preferred_name = models.CharField(max_length=32, blank=True, null=False, default="")
    surname = models.CharField(max_length=32, blank=False, null=False, default="UNKNOWN")
    # ADDRESS
    street_address = models.CharField(max_length=64, blank=True, null=False, default="")
    postal_code = models.CharField(max_length=64, blank=True, null=False, default="")
    city = models.CharField(max_length=64, blank=True, null=False, default="")
    # https://pypi.python.org/pypi/django-countries/1.0.1
    country = CountryField(blank_label="Välj land", blank=True, null=False, default="")
    # CONTACT INFO
    phone = models.CharField(max_length=128, blank=True, null=False, default="")
    email = models.CharField(max_length=64, blank=True, null=False, default="")
    # DATE OF BIRTH
    birth_date = models.DateField(blank=True, null=True)
    # STUDIES
    student_id = models.CharField(max_length=10, blank=True, null=True, default=None, unique=True)
    degree_programme = models.CharField(max_length=256, blank=True, null=False)
    enrolment_year = models.IntegerField(blank=True, null=True)
    graduated = models.BooleanField(default=False)
    graduated_year = models.IntegerField(blank=True, null=True)
    # OTHER
    dead = models.BooleanField(default=False)
    # TODO: separate consent to own table
    subscribed_to_modulen = models.BooleanField(default=False)
    allow_publish_info = models.BooleanField(default=False)
    allow_studentbladet = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    # IT-username and BILL
    username = models.CharField(max_length=32, blank=False, null=True, editable=False, unique=True)
    bill_code = models.CharField(max_length=8, blank=False, null=True, editable=False)

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        # Store original email so we can check if it has changed on save
        self._original_email = self.email

    '''
    Names are complicated...
    - Given names (or first names)
        * Mandatory
        * Can be one or many
    - Preferred name
        * Not mandatory
        * If present, must be one of the given names (but that restriction is not currently implemented)
        * If empty, it is assumed that the first given name is the preferred name
    - Surname
        * Mandatory
        * Can be one or many
        * Can include prefixes such as 'von' or 'af' that need to be taken into consideration when sorting is applied. For example, 'von Numers' should be sorted by 'N', not 'V'.

    Members can choose to not have their information public, meaning that at least contact information such as email, phone number and addresses should be hidden to normal users, but does this also apply to for example middle names ? If one don't want thier middle names to be shown they could just request them to be removed, since we don't really need them for anything else than for uniquely identifying people with the same first and last names. But on the other hand we don't really want people actually removing their middle name since the amount of duplicate names is not negligible, not that I think anyone actually has a problem revealing their middle names... The compromise would be to write the non-preferred given names as initials, such as 'Kalle C J Anka' or 'K-G Kalle M Anka'.

    So there need to be at least 4 different name methods/properties:
    - full_name 
        = '<given_names> <surname>'
    - full_name_with_initials
        = '<preferred_name> <remaining given_name initials> <surname>'
    - full_name_for_sorting
        = '<surname with removed prefix> <given_names>'
    - full_name_with_initials_for_sorting
        = '<surname with removed prefix> <preferred_name> <remaining given_name initials>'
    '''

    def get_preferred_name(self):
        return self.preferred_name or self.given_names.split()[0]

    def get_given_names_with_initials(self):
        preferred_name = self.get_preferred_name()
        names = [n if n == preferred_name else n[0] for n in self.given_names.split()]
        return " ".join(names)

    def get_surname_without_prefixes(self):
        # Surname prefixes such as 'von' or 'af' should always be written out, but is usually not considered when sorting names alphabethically. There are even surnames with more than one prefix. For example, 'von der Leyen' should be sorted by 'L'.

        # Let's assume the prefixes in question are always written with lowercase, and that everything written in all lowercase are prefixes...
        surname = self.surname
        return surname.lstrip('abcdefghijklmnopqrstuvwxyzåäö ') or surname.split()[-1]

    # Used for the side bar among other things
    @property
    def name(self):
        return self.full_name

    @property
    def common_name(self):
        return f'{self.get_preferred_name()} {self.surname}'

    @property
    def full_name(self):
        return f'{self.given_names} {self.surname}'

    @property
    def public_full_name(self):
        if self.showContactInformation():
            return self.full_name
        return f'{self.get_given_names_with_initials()} {self.surname}'

    @property
    def full_name_for_sorting(self):
        return f'{self.get_surname_without_prefixes()}, {self.given_names}'

    @property
    def public_full_name_for_sorting(self):
        if self.showContactInformation():
            return self.full_name_for_sorting
        return f'{self.get_surname_without_prefixes()}, {self.get_given_names_with_initials()}'

    def _get_most_recent_member_type_name(self):
        member_type = self.getMostRecentMemberType()

        if member_type:
            return member_type.get_type_display()
        else:
            return ""

    current_member_type = property(_get_most_recent_member_type_name)

    def __str__(self):
        return self.public_full_name

    @property
    def full_address(self):
        country = 'Finland'
        if self.country.name:
            country = str(self.country.name)
        city = f'{self.postal_code} {self.city}'.strip()
        address_parts = [self.street_address, city, country]
        return ", ".join([s for s in address_parts if s])

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = None
        if not self.student_id:
            self.student_id = None

        # Sync email to LDAP if changed
        error = None
        if self.username and self.email != self._original_email:
            from api.ldap import LDAPAccountManager
            from ldap import LDAPError
            try:
                with LDAPAccountManager() as lm:
                    lm.change_email(self.username, self.email)
            except LDAPError as e:
                # Could not update LDAP, save other fields but keep original email
                self.email = self._original_email
                # Raise an error anyway to notify user
                error = e

        super(Member, self).save(*args, **kwargs)
        if error:
            raise error

    def getMostRecentMemberType(self):
        types = self.member_types.all()

        if (len(types)) == 0:
            return None

        ordinarie = next((x for x in types if x.type == "OM"), None)
        if ordinarie and not ordinarie.end_date:
            return ordinarie

        stalm = next((x for x in types if x.type == "ST"), None)
        if stalm and not stalm.end_date:
            return stalm

        return None

    def shouldBeStalm(self):
        ''' Used to find Juniorstalmar members that should magically become stalmar somehow '''
        return not self.isValidMember() and ("JS" in [x.type for x in MemberType.objects.filter(member=self)])

    def isValidMember(self):
        memberType = self.getMostRecentMemberType()
        return memberType is not None and (memberType.type == "OM" or memberType.type == "ST")

    @property
    def phux_year(self):
        types = self.member_types.all()
        # XXX: Do we need to take into account multiple Phux MemberTypes?
        member_type_phux = next((x for x in types if x.type == "PH"), None)
        return member_type_phux.begin_date.year if member_type_phux else None

    def showContactInformation(self):
        return self.allow_publish_info and self.isValidMember() and not self.dead

    @property
    def decoration_ownerships_by_date(self):
        l = list(self.decoration_ownerships.all())
        DecorationOwnership.order_by(l, 'name')
        DecorationOwnership.order_by(l, 'date', True)
        return l

    @property
    def functionaries_by_date(self):
        l = list(self.functionaries.all())
        Functionary.order_by(l, 'name')
        Functionary.order_by(l, 'date', True)
        return l

    @property
    def group_memberships_by_date(self):
        l = list(self.group_memberships.all())
        GroupMembership.order_by(l, 'name')
        GroupMembership.order_by(l, 'date', True)
        return l

    @classmethod
    def order_by(cls, members_list, by, reverse=False):
        if by == 'name':
            key = lambda m: strxfrm(m.full_name_for_sorting)
        else:
            return
        members_list.sort(key=key, reverse=reverse)


class DecorationOwnershipManager(models.Manager):
    def year(self, year):
        return self.get_queryset().select_related('member', 'decoration').filter(acquired__year=year)

    def year_ordered(self, year):
        l = list(self.year(year))
        DecorationOwnership.order_by(l, 'member')
        DecorationOwnership.order_by(l, 'name')
        return l

class DecorationOwnership(SuperClass):
    objects = DecorationOwnershipManager()
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="decoration_ownerships")
    decoration = models.ForeignKey("Decoration", on_delete=models.CASCADE, related_name="ownerships")
    acquired = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.decoration.name, self.member)

    @classmethod
    def order_by(cls, ownerships_list, by, reverse=False):
        if by == 'date':
            key = attrgetter('acquired')
        elif by == 'name':
            key = lambda do: strxfrm(do.decoration.name)
        elif by == 'member':
            key = lambda do: strxfrm(do.member.full_name_for_sorting)
        else:
            return
        ownerships_list.sort(key=key, reverse=reverse)


class DecorationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(count=Count('ownerships'))

    def all_by_name(self):
        l = list(self.get_queryset())
        Decoration.order_by(l, 'name')
        return l

    def get_prefetched_or_404(self, decoration_id):
        '''
        This is done in 2 queries:
        1. SELECT Decoration WHERE id=decoration_id
        2. SELECT DecorationOwnership WHERE decoration__id=decoration_id
        '''
        queryset = Decoration.objects.prefetch_related(
            Prefetch('ownerships', queryset=DecorationOwnership.objects.select_related('member')),
        )
        return get_object_or_404(queryset, id=decoration_id)

class Decoration(SuperClass):
    objects = DecorationManager()
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def ownerships_by_date(self):
        l = list(self.ownerships.all())
        DecorationOwnership.order_by(l, 'member')
        DecorationOwnership.order_by(l, 'date', True)
        return l

    @classmethod
    def order_by(cls, decorations_list, by, reverse=False):
        if by == 'name':
            key = lambda d: strxfrm(d.name)
        else:
            return
        decorations_list.sort(key=key, reverse=reverse)

class GroupMembership(SuperClass):
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        unique_together = (("member", "group"),)

    @classmethod
    def order_by(cls, memberships_list, by, reverse=False):
        if by == 'date':
            key = attrgetter('group.end_date', 'group.begin_date')
        elif by == 'name':
            key = lambda gm: strxfrm(gm.group.grouptype.name)
        elif by == 'member':
            key = lambda gm: strxfrm(gm.member.full_name_for_sorting)
        else:
            return
        memberships_list.sort(key=key, reverse=reverse)


class GroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_members=Count('memberships', distinct=True))

    def year(self, year):
        return self.get_queryset().prefetch_related(
            Prefetch(
                'memberships',
                queryset=GroupMembership.objects.select_related('member')
            ),
            'grouptype'
        ).filter(begin_date__lte=datetime.date(int(year), 12, 31), end_date__gte=datetime.date(int(year), 1, 1), num_members__gt=0)

    def year_ordered_and_counts(self, year):
        queryset = self.year(year)
        gm_counts = queryset.aggregate(total=Count('memberships__member__id'), unique=Count('memberships__member__id', distinct=True))
        l = list(queryset)
        Group.order_by(l, 'name')
        return l, gm_counts['total'], gm_counts['unique']

class Group(SuperClass):
    objects = GroupManager()
    grouptype = models.ForeignKey("GroupType", on_delete=models.CASCADE, related_name="groups")
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0}: {1} - {2}".format(self.grouptype.name, self.begin_date, self.end_date)

    @property
    def duration_string(self):
        return create_duration_string(self.begin_date, self.end_date)

    @property
    def memberships_by_member(self):
        l = list(self.memberships.all())
        GroupMembership.order_by(l, 'member')
        return l

    @classmethod
    def order_by(cls, groups_list, by, reverse=False):
        if by == 'date':
            key = attrgetter('end_date', 'begin_date')
        elif by == 'name':
            key = lambda g: strxfrm(g.grouptype.name)
        else:
            return
        groups_list.sort(key=key, reverse=reverse)

class GroupTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            count=Count('groups', distinct=True),
            count_non_empty=Count('groups', distinct=True, filter=Q(groups__memberships__gt=0)),
            count_members_total=Count('groups__memberships'),
            count_members_unique=Count('groups__memberships__member', distinct=True),
        )

    def all_by_name(self):
        l = list(self.get_queryset())
        GroupType.order_by(l, 'name')
        return l

    def get_prefetched_or_404(self, group_type_id):
        '''
        This is done in 3 queries:
        1. SELECT GroupType WHERE id=group_type_id
        2. SELECT Group WHERE grouptype__id=group_type_id
        3. SELECT GroupMembership WHERE group__id IN ^
        '''
        queryset = GroupType.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all()),
            Prefetch('groups__memberships', queryset=GroupMembership.objects.select_related('member')),
        )
        return get_object_or_404(queryset, id=group_type_id)

class GroupType(SuperClass):
    objects = GroupTypeManager()
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def groups_by_date(self):
        l = list(self.groups.all())
        Group.order_by(l, 'date', True)
        return l

    @classmethod
    def order_by(cls, grouptypes_list, by, reverse=False):
        if by == 'name':
            key = lambda gt: strxfrm(gt.name)
        else:
            return
        grouptypes_list.sort(key=key, reverse=reverse)


class FunctionaryManager(models.Manager):
    def year(self, year):
        return self.get_queryset().select_related('member', 'functionarytype').filter(begin_date__lte=datetime.date(int(year), 12, 31), end_date__gte=datetime.date(int(year), 1, 1))

    def year_ordered_and_unique(self, year):
        queryset = self.year(year)
        unique_count = queryset.aggregate(count=Count('member__id', distinct=True))['count']
        l = list(queryset)
        Functionary.order_by(l, 'member')
        Functionary.order_by(l, 'date')
        Functionary.order_by(l, 'name')
        return l, unique_count

class Functionary(SuperClass):
    objects = FunctionaryManager()
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name="functionaries")
    functionarytype = models.ForeignKey("FunctionaryType", on_delete=models.CASCADE, related_name="functionaries")
    begin_date = models.DateField()
    end_date = models.DateField()

    @property
    def duration_string(self):
        return create_duration_string(self.begin_date, self.end_date)

    def _get_str_member(self):
        return "{0} - {1}: {2}".format(self.begin_date, self.end_date, self.member)

    def _get_str_type(self):
        return "{0}: {1} - {2}".format(self.functionarytype, self.begin_date, self.end_date)

    str_member = property(_get_str_member)
    str_type = property(_get_str_type)

    def _get_funcationary_type_id(self):
        return self.functionarytype.id

    functionary_type_id = property(_get_funcationary_type_id)

    class Meta:
        unique_together = (("member", "functionarytype", "begin_date", "end_date"),)

    def __str__(self):
        return "{0}: {1} - {2}, {3}".format(self.functionarytype, self.begin_date, self.end_date, self.member)

    @classmethod
    def order_by(cls, functionaries_list, by, reverse=False):
        if by == 'date':
            key = attrgetter('end_date', 'begin_date')
        elif by == 'name':
            key =  lambda f: strxfrm(f.functionarytype.name)
        elif by == 'member':
            key = lambda f: strxfrm(f.member.full_name_for_sorting)
        else:
            return
        functionaries_list.sort(key=key, reverse=reverse)

class FunctionaryTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
        count=Count('functionaries'),
        count_unique=Count('functionaries__member', distinct=True),
    )

    def all_by_name(self):
        l = list(self.get_queryset())
        FunctionaryType.order_by(l, 'name')
        return l

    def get_prefetched_or_404(self, functionary_type_id):
        '''
        This is done in 2 queries:
        1. SELECT FunctionaryType WHERE id=functionary_type_id
        2. SELECT Functionary WHERE functionarytype__id=functionary_type_id
        '''
        queryset = FunctionaryType.objects.prefetch_related(
            Prefetch('functionaries', queryset=Functionary.objects.select_related('member')),
        )
        return get_object_or_404(queryset, id=functionary_type_id)

class FunctionaryType(SuperClass):
    objects = FunctionaryTypeManager()
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def functionaries_by_date(self):
        l = list(self.functionaries.all())
        Functionary.order_by(l, 'member')
        Functionary.order_by(l, 'date', True)
        return l

    @classmethod
    def order_by(cls, functionarytypes_list, by, reverse=False):
        if by == 'name':
            key = lambda ft: strxfrm(ft.name)
        else:
            return
        functionarytypes_list.sort(key=key, reverse=reverse)


class MemberTypeManager(models.Manager):
    def begin_year(self, year):
        return self.get_queryset().select_related('member').filter(begin_date__year=year)

    def ordinary_members_begin_year(self, year):
        return self.begin_year(year).filter(type='OM')

    def ordinary_members_begin_year_ordered(self, year):
        l = list(self.ordinary_members_begin_year(year))
        MemberType.order_by(l, 'member')
        return l

    def stalms_begin_year(self, year):
        return self.begin_year(year).filter(type='ST')

    def stalms_begin_year_ordered(self, year):
        l = list(self.stalms_begin_year(year))
        MemberType.order_by(l, 'member')
        return l


class MemberType(SuperClass):
    objects = MemberTypeManager()
    TYPES = (
        ("PH", "Phux"),
        ("OM", "Ordinarie Medlem"),
        ("JS", "JuniorStÄlM"),
        ("ST", "StÄlM"),
        ("FG", "Färdig"),
        ("EM", "Ej längre medlem"),
        ("VP", "Viktig person"),
        ("KA", "Kanslist"),
        ("IM", "Inte medlem"),
        ("KE", "Kanslist emerita"),

    )
    member = models.ForeignKey("Member", on_delete=models.CASCADE, related_name='member_types')
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    type = models.CharField(max_length=2, choices=TYPES, default="PH")

    def __str__(self):
        return "{0}: {1}-{2}".format(
            self.get_type_display(), self.begin_date, (self.end_date if self.end_date else ">")
            )

    @classmethod
    def order_by(cls, membertypes_list, by, reverse=False):
        if by == 'begin_date':
            key = lambda mt: mt.begin_date
        elif by == 'end_date':
            key = lambda mt: mt.end_date or datetime.date(9999, 12, 31)
        elif by == 'member':
            key = lambda mt: strxfrm(mt.member.full_name_for_sorting)
        else:
            return
        membertypes_list.sort(key=key, reverse=reverse)
