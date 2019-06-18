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


class MemberSerializer(serializers.ModelSerializer):
    country = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)
    nationality = SerializableCountryField(allow_blank=True, choices=Countries(), required=False)

    class Meta:
        model = Member
        fields = '__all__'


# Groups

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = '__all__'


# Functionaries

class FunctionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Functionary
        fields = '__all__'


class FunctionaryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionaryType
        fields = '__all__'


# Decorations

class DecorationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = '__all__'


class DecorationOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecorationOwnership
        fields = '__all__'


# MemberTypes

class MemberTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberType
        fields = '__all__'


# Applicant

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
