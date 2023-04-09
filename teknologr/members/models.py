# -*- coding: utf-8 -*-

from django.db import models
from django_countries.fields import CountryField


class SuperClass(models.Model):
    # This class is the base of everything
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(SuperClass):
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

    def _get_full_name(self):
        return "%s %s" % (self.given_names, self.surname)

    def _get_full_preferred_name(self):
        first_name = self.preferred_name if self.preferred_name else self.given_names.split()[0]
        return "%s %s" % (first_name, self.surname)

    def _get_most_recent_member_type_name(self):
        member_type = self.getMostRecentMemberType()

        if member_type:
            return member_type.get_type_display()
        else:
            return ""

    full_name = property(_get_full_name)
    name = property(_get_full_name)
    full_preferred_name = property(_get_full_preferred_name)
    current_member_type = property(_get_most_recent_member_type_name)

    def __str__(self):
        return self.full_name

    def _get_full_address(self):
        country = 'Finland'
        if self.country.name:
            country = str(self.country.name)
        address_parts = [self.street_address, self.city, country]
        if self.postal_code:
            address_parts.insert(1, self.postal_code)
        return ", ".join(address_parts)
        # return "%s, %s, %s, %s" % ()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = None
        if not self.student_id:
            self.student_id = None
        if not self.preferred_name:
            self.preferred_name = self.given_names.split()[0]

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
        types = MemberType.objects.filter(member=self).order_by()

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
        phuxYear = MemberType.objects.filter(member=self).filter(type='PH').order_by('begin_date')
        phux_year_begin_date = len(phuxYear) and phuxYear[0].begin_date
        return phux_year_begin_date.year if phux_year_begin_date else None

    def showContactInformation(self):
        return self.allow_publish_info and self.isValidMember() and not self.dead


class DecorationOwnership(SuperClass):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    decoration = models.ForeignKey("Decoration", on_delete=models.CASCADE, related_name="ownerships")
    acquired = models.DateField()

    def __str__(self):
        return "%s - %s" % (self.decoration.name, self.member.full_name)


class Decoration(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class GroupMembership(SuperClass):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        unique_together = (("member", "group"),)


class Group(SuperClass):
    grouptype = models.ForeignKey("GroupType", on_delete=models.CASCADE, related_name="groups")
    begin_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0}: {1} - {2}".format(self.grouptype.name, self.begin_date, self.end_date)


class GroupType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Functionary(SuperClass):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    functionarytype = models.ForeignKey("FunctionaryType", on_delete=models.CASCADE, related_name="functionaries")
    begin_date = models.DateField()
    end_date = models.DateField()

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


class FunctionaryType(SuperClass):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    comment = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class MemberType(SuperClass):
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
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    begin_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    type = models.CharField(max_length=2, choices=TYPES, default="PH")

    def __str__(self):
        return "{0}: {1}-{2}".format(
            self.get_type_display(), self.begin_date, (self.end_date if self.end_date else ">")
            )
