from django_countries import Countries
from rest_framework import serializers
from members.models import *
from registration.models import Applicant


class SerializableCountryField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)

class IdAndName(serializers.Serializer):
    ''' Helper class for serializing small partial objects '''
    def to_representation(self, obj):
        return {'id': obj.id, 'name': obj.name}

class IdAndPublicFullName(serializers.Serializer):
    ''' Helper class for serializing partial Member objects '''
    def to_representation(self, obj):
        return {'id': obj.id, 'name': obj.public_full_name}

class BaseSerializer(serializers.ModelSerializer):
    ''' Base class for all our serializers that captures the 'detail' keyword '''
    def __init__(self, *args, detail=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = detail


# Members

class MemberSerializerFull(BaseSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)

    class Meta:
        model = Member
        fields = '__all__'
class MemberSerializerAdmin(MemberSerializerFull):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        functionaries = obj.functionaries.all()
        group_memberships = obj.group_memberships.all()
        decoration_ownerships = obj.decoration_ownerships.all()

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

        return data

class MemberSerializerPublic(MemberSerializerAdmin):
    class Meta:
        model = Member
        fields = ('id', 'country', 'given_names', 'preferred_name', 'surname', 'street_address', 'postal_code', 'city', 'phone', 'email', 'degree_programme', 'enrolment_year', 'graduated', 'graduated_year', )

    def to_representation(self, obj):
        # Get the original representation
        data = super().to_representation(obj)

        # Modify Member data if necessary
        if not obj.showContactInformation():
            # Remove contact information
            for c in ['country', 'street_address', 'postal_code', 'city', 'phone', 'email']:
                data.pop(c)

            # Convert given names to initials
            data['given_names'] = obj.get_given_names_with_initials()

        return data


# GroupTypes, Groups and GroupMemberships

class GroupTypeSerializerFull(BaseSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'
class GroupTypeSerializerAdmin(GroupTypeSerializerFull):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        groups = obj.groups.all()

        # Add count of related objects
        data['n_groups'] = len(groups)

        return data
class GroupTypeSerializerPublic(GroupTypeSerializerAdmin):
    class Meta:
        model = GroupType
        fields = ('id', 'name', 'comment', )

class GroupSerializerFull(BaseSerializer):
    class Meta:
        model = Group
        fields = '__all__'
class GroupSerializerAdmin(GroupSerializerFull):
    grouptype = IdAndName()

    def to_representation(self, obj):
        data = super().to_representation(obj)
        memberships = obj.memberships.all()

        # Add count of related objects
        data['n_members'] = len(memberships)

        # XXX: Should it be n_members/members or n_memberships/memberships (or some other combination)? It feels silly having a list of memberships that looks like [{id, member}, ..], so skipping over the actual GroupMembership objects here. Could of course add a field called membership_id, but I don't see that being needed...

        # Add the actual related objects if detail view
        if self.detail:
            data['members'] = [{
                'id': gm.member.id,
                'name': gm.member.public_full_name,
            } for gm in memberships]

        return data
class GroupSerializerPublic(GroupSerializerAdmin):
    class Meta:
        model = Group
        fields = ('id', 'grouptype', 'begin_date', 'end_date', )

class GroupMembershipSerializerFull(BaseSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'
class GroupMembershipSerializerAdmin(GroupMembershipSerializerFull):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        group = obj.group

        data['member'] = IdAndName(obj.member).data
        data['group'] = {
            'id': group.id,
            'begin_date': group.begin_date,
            'end_date': group.end_date,
            'grouptype': IdAndName(group.grouptype).data
        }

        return data
class GroupMembershipSerializerPublic(GroupMembershipSerializerAdmin):
    class Meta:
        model = GroupMembership
        fields = ('id', 'group', 'member', )


# FunctionaryTypes and Functionaries

class FunctionaryTypeSerializerFull(BaseSerializer):
    class Meta:
        model = FunctionaryType
        fields = '__all__'

class FunctionaryTypeSerializerAdmin(FunctionaryTypeSerializerFull):

    def to_representation(self, obj):
        data = super().to_representation(obj)
        functionaries = obj.functionaries.all()

        # Add count of related objects
        data['n_functionaries'] = len(functionaries)

        # Add the actual related objects if detail view
        if self.detail:
            data['functionaries'] = [{
                'id': f.id,
                'begin_date': f.begin_date,
                'end_date': f.end_date,
                # XXX: Full name for staff?
                'member': IdAndPublicFullName(f.member).data,
            } for f in functionaries]

        return data
class FunctionaryTypeSerializerPublic(FunctionaryTypeSerializerAdmin):
    class Meta:
        model = FunctionaryType
        fields = ('id', 'name', 'comment', )

class FunctionarySerializerFull(BaseSerializer):
    class Meta:
        model = Functionary
        fields = '__all__'
class FunctionarySerializerAdmin(FunctionarySerializerFull):
    functionarytype = IdAndName()
    member = IdAndName()
class FunctionarySerializerPublic(FunctionarySerializerAdmin):
    member = IdAndPublicFullName()

    class Meta:
        model = Functionary
        fields = ('id', 'functionarytype', 'member', 'begin_date', 'end_date', )


# Decorations and DecorationOwnerships

class DecorationSerializerFull(BaseSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'
class DecorationSerializerAdmin(DecorationSerializerFull):

    def to_representation(self, obj):
        data = super().to_representation(obj)
        ownerships = obj.ownerships.all()

        # Add count of related objects
        data['n_ownerships'] = len(ownerships)

        # Add the actual related objects if detail view
        if self.detail:
            data['ownerships'] = [{
                'id': do.id,
                'acquired': do.acquired,
                # XXX: Full name for staff?
                'member': IdAndPublicFullName(do.member).data,
            } for do in ownerships]

        return data
class DecorationSerializerPublic(DecorationSerializerAdmin):
    class Meta:
        model = Decoration
        fields = ('id', 'name', 'comment', )

class DecorationOwnershipSerializerFull(BaseSerializer):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'
class DecorationOwnershipSerializerAdmin(DecorationOwnershipSerializerFull):
    decoration = IdAndName()
    member = IdAndName()
class DecorationOwnershipSerializerPublic(DecorationOwnershipSerializerAdmin):
    member = IdAndPublicFullName()

    class Meta:
        model = DecorationOwnership
        fields = ('id', 'decoration', 'member', 'acquired', )


# MemberTypes

class MemberTypeSerializerFull(BaseSerializer):
    class Meta:
        model = MemberType
        fields = '__all__'
class MemberTypeSerializerAdmin(MemberTypeSerializerFull):
    member = IdAndName()


# Applicant

class ApplicantSerializerFull(BaseSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
