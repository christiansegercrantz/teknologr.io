from django_countries import Countries
from rest_framework import serializers
from members.models import *
from registration.models import Applicant


class SerializableCountryField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return ''  # instead of `value` as Country(u'') is not serializable
        return super(SerializableCountryField, self).to_representation(value)

# Serializers define the API representation.


# Members

class MemberSerializerAdmin(serializers.ModelSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)

    class Meta:
        model = Member
        fields = '__all__'

class MemberSerializerPublic(serializers.ModelSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)

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

class MemberSerializerPartial(serializers.ModelSerializer):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'name': obj.public_full_name,
        }


# GroupTypes, Groups and GroupMemberships

class GroupTypeSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'
class GroupTypeSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = ('id', 'name', 'comment', )
class GroupTypeSerializerPartial(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = ('id', 'name', )

class GroupSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
class GroupSerializerAdmin(GroupSerializerFull):
    # NOTE: Important to use qs.select_related('grouptype'), or else each object will hit the db with an additional fetch query
    grouptype = GroupTypeSerializerPartial()
class GroupSerializerPublic(GroupSerializerAdmin):
    class Meta:
        model = Group
        fields = ('id', 'grouptype', 'begin_date', 'end_date', )

class GroupMembershipSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'
class GroupMembershipSerializerAdmin(GroupMembershipSerializerFull):
    # NOTE: Important to use qs.select_related('group', 'group__grouptype', 'member), or else each object will hit the db with three additional fetch queries
    group = GroupSerializerPublic()
    member = MemberSerializerPartial()
class GroupMembershipSerializerPublic(GroupMembershipSerializerAdmin):
    class Meta:
        model = GroupMembership
        fields = ('id', 'group', 'member', )


# FunctionaryTypes and Functionaries

class FunctionaryTypeSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = FunctionaryType
        fields = '__all__'
class FunctionaryTypeSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = FunctionaryType
        fields = ('id', 'name', 'comment', )
class FunctionaryTypeSerializerPartial(serializers.ModelSerializer):
    class Meta:
        model = FunctionaryType
        fields = ('id', 'name', )

class FunctionarySerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Functionary
        fields = '__all__'
class FunctionarySerializerAdmin(FunctionarySerializerFull):
    # NOTE: Important to use qs.select_related('functionarytype', 'member'), or else each object will hit the db with two additional fetch queries
    functionarytype = FunctionaryTypeSerializerPartial()
    member = MemberSerializerPartial()
class FunctionarySerializerPublic(FunctionarySerializerAdmin):
    class Meta:
        model = Functionary
        fields = ('id', 'functionarytype', 'member', 'begin_date', 'end_date', )


# Decorations and DecorationOwnerships

class DecorationSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'
class DecorationSerializerPublic(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = ('id', 'name', 'comment', )
class DecorationSerializerPartial(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = ('id', 'name', )


class DecorationOwnershipSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'
class DecorationOwnershipSerializerAdmin(DecorationOwnershipSerializerFull):
    # NOTE: Important to use qs.select_related('decoration', 'member'), or else each object will hit the db with two additional fetch queries
    decoration = DecorationSerializerPartial()
    member = MemberSerializerPartial()
class DecorationOwnershipSerializerPublic(DecorationOwnershipSerializerAdmin):
    class Meta:
        model = DecorationOwnership
        fields = ('id', 'decoration', 'member', 'acquired', )


# MemberTypes

class MemberTypeSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = MemberType
        fields = '__all__'
class MemberTypeSerializerAdmin(MemberTypeSerializerFull):
    # NOTE: Important to use qs.select_related('member'), or else each object will hit the db with an additional fetch query
    member = MemberSerializerPartial()


# Applicant

class ApplicantSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
