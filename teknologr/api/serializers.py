from django_countries import Countries
from rest_framework import serializers
from members.models import *
from registration.models import Applicant


class SerializableCountryField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)

class BaseSerializer(serializers.ModelSerializer):
    '''
    Base class for all our serializers that automatically removes staff-only fields for normal users. It also captures the 'detail' keyword that signifies that the serializer is used for a detail API view instead, for which inherited classes add more details to the representation.
    '''

    STAFF_ONLY = []

    def __init__(self, *args, detail=False, is_staff=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = detail
        self.is_staff = is_staff

    def remove_fields(self, fields):
        ''' Removed fields from this serializer by removing them from self.fields, which works because that is a @cached_property '''
        for field in fields:
            if field in self.fields:
                self.fields.pop(field)

    def to_representation(self, instance):
        # Remove staff only fields for normal users
        if not self.is_staff:
            self.remove_fields(self.STAFF_ONLY + ['created', 'modified'])
        return super().to_representation(instance)

    def get_minimal_id_name(self, instance):
        return {'id': instance.id, 'name': instance.name}

    def get_minimal_member(self, member):
        return {'id': member.id, 'name': member.name if self.is_staff else member.public_full_name}


# Members

class MemberSerializer(BaseSerializer):
    STAFF_ONLY = ['birth_date', 'student_id', 'dead', 'subscribed_to_modulen', 'allow_publish_info', 'allow_studentbladet', 'comment', 'username', 'bill_code']

    country = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)

    class Meta:
        model = Member
        fields = '__all__'

    def to_representation(self, instance):
        hide = not self.is_staff and not instance.showContactInformation()
        if hide:
            self.remove_fields(['country', 'street_address', 'postal_code', 'city', 'phone', 'email'])

        data = super().to_representation(instance)
        functionaries = instance.functionaries.all()
        group_memberships = instance.group_memberships.all()
        decoration_ownerships = instance.decoration_ownerships.all()

        # Add counts of related objects
        # XXX: Could annotate the Member objects with count fields beforehand...
        data['n_functionaries'] = len(functionaries)
        data['n_groups'] = len(group_memberships)
        data['n_decorations'] = len(decoration_ownerships)

        # Add the actual related objects if detail view
        if self.detail:
            data['functionaries'] = [{
                'functionarytype': {'id': f.functionarytype.id, 'name': f.functionarytype.name},
                'begin_date': f.begin_date,
                'end_date': f.end_date,
            } for f in functionaries]
            data['groups'] = [{
                'grouptype': {'id': gm.group.grouptype.id, 'name': gm.group.grouptype.name},
                'begin_date': gm.group.begin_date,
                'end_date': gm.group.end_date,
            } for gm in group_memberships]
            data['decorations'] = [{
                'decoration': {'id': do.decoration.id, 'name': do.decoration.name},
                'acquired': do.acquired,
            } for do in decoration_ownerships]

        # Modify certain fields if necessary
        if hide:
            data['given_names'] = instance.get_given_names_with_initials()

        return data


# GroupTypes, Groups and GroupMemberships

class GroupTypeSerializer(BaseSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        groups = instance.groups.all()

        # Add count of related objects
        data['n_groups'] = len(groups)

        # Add the actual related objects if detail view
        if self.detail:
            data['groups'] = [{
                'id': g.id,
                'begin_date': g.begin_date,
                'end_date': g.end_date,
                'n_members': g.num_members
            } for g in groups]

        return data

class GroupSerializer(BaseSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        memberships = instance.memberships.all()

        # Add count of related objects
        data['n_members'] = len(memberships)

        # XXX: Should it be n_members/members or n_memberships/memberships (or some other combination)? It feels silly having a list of memberships that looks like [{id, member}, ..], so skipping over the actual GroupMembership objects here. Could of course add a field called membership_id, but I don't see that being needed...

        # Add the actual related objects if detail view
        if self.detail:
            data['members'] = [{
                'id': gm.member.id,
                'name': gm.member.public_full_name,
            } for gm in memberships]

        # Always show the grouptype as a subobject
        data['grouptype'] = self.get_minimal_id_name(instance.grouptype)

        return data

class GroupMembershipSerializer(BaseSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        group = instance.group

        data['member'] = self.get_minimal_member(instance.member)
        data['group'] = {
            'id': group.id,
            'begin_date': group.begin_date,
            'end_date': group.end_date,
            'grouptype': self.get_minimal_id_name(group.grouptype)
        }

        return data


# FunctionaryTypes and Functionaries

class FunctionaryTypeSerializer(BaseSerializer):
    class Meta:
        model = FunctionaryType
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        functionaries = instance.functionaries.all()

        # Add count of related objects
        data['n_functionaries'] = len(functionaries)

        # Add the actual related objects if detail view
        if self.detail:
            data['functionaries'] = [{
                'id': f.id,
                'begin_date': f.begin_date,
                'end_date': f.end_date,
                'member': self.get_minimal_member(f.member),
            } for f in functionaries]

        return data

class FunctionarySerializer(BaseSerializer):
    class Meta:
        model = Functionary
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['functionarytype'] = self.get_minimal_id_name(instance.functionarytype)
        data['member'] = self.get_minimal_member(instance.member)
        return data


# Decorations and DecorationOwnerships

class DecorationSerializer(BaseSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        ownerships = instance.ownerships.all()

        # Add count of related objects
        data['n_ownerships'] = len(ownerships)

        # Add the actual related objects if detail view
        if self.detail:
            data['ownerships'] = [{
                'id': do.id,
                'acquired': do.acquired,
                'member': self.get_minimal_member(do.member),
            } for do in ownerships]

        return data

class DecorationOwnershipSerializer(BaseSerializer):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['decoration'] = self.get_minimal_id_name(instance.decoration)
        data['member'] = self.get_minimal_member(instance.member)
        return data


# MemberTypes

class MemberTypeSerializer(BaseSerializer):
    class Meta:
        model = MemberType
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['member'] = self.get_minimal_member(instance.member)
        return data


# Applicant

class ApplicantSerializer(BaseSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
