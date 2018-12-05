from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from members.models import GroupMembership, Member, Group
from api.ldap import LDAPAccountManager
from ldap import LDAPError
from api.bill import BILLAccountManager, BILLException
from rest_framework_csv import renderers as csv_renderer
from api.mailutils import mailNewPassword
from collections import defaultdict
from datetime import datetime

# Create your views here.

# ViewSets define the view behavior.

# Members


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


# Groups

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupTypeViewSet(viewsets.ModelViewSet):
    queryset = GroupType.objects.all()
    serializer_class = GroupTypeSerializer


class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer


@api_view(['POST'])
def memberListSave(request):
    gid = request.data.get('group')
    members = request.data.get('member').strip("|").split("|")

    for mid in members:
        # get_or_create is used to ignore duplicates
        GroupMembership.objects.get_or_create(member_id=int(mid), group_id=int(gid))

    return Response(status=200)


# Functionaries

class FunctionaryViewSet(viewsets.ModelViewSet):
    queryset = Functionary.objects.all()
    serializer_class = FunctionarySerializer


class FunctionaryTypeViewSet(viewsets.ModelViewSet):
    queryset = FunctionaryType.objects.all()
    serializer_class = FunctionaryTypeSerializer


# Decorations

class DecorationViewSet(viewsets.ModelViewSet):
    queryset = Decoration.objects.all()
    serializer_class = DecorationSerializer


class DecorationOwnershipViewSet(viewsets.ModelViewSet):
    queryset = DecorationOwnership.objects.all()
    serializer_class = DecorationOwnershipSerializer


# MemberTypes

class MemberTypeViewSet(viewsets.ModelViewSet):
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeSerializer


# User accounts

class LDAPAccountView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)
        result = {}
        with LDAPAccountManager() as lm:
            try:
                result = {'username': member.username, 'groups': lm.get_ldap_groups(member.username)}
            except LDAPError as e:
                return Response(str(e), status=400)

        return Response(result, status=200)

    def post(self, request, member_id):
        # Create LDAP and BILL accounts for given user
        member = get_object_or_404(Member, id=member_id)
        username = request.data.get('username')
        password = request.data.get('password')
        mailToUser = request.data.get('mail_to_user')
        if not username or not password:
            return Response("username or password field missing", status=400)

        if member.username:
            return Response("Member already has LDAP account", status=400)

        with LDAPAccountManager() as lm:
            try:
                lm.add_account(member, username, password)
                if mailToUser:
                    status = mailNewPassword(member, password)
                    if not status:
                        return Response("Password changed, failed to send mail", status=500)
            except LDAPError as e:
                return Response(str(e), status=400)

        # Store account details
        member.username = username
        member.save()

        # TODO: Send mail to user to notify about new account?

        return Response(status=200)

    def delete(self, request, member_id):
        # Delete LDAP account for a given user
        member = get_object_or_404(Member, id=member_id)

        if not member.username:
            return Response("Member has no LDAP account", status=400)
        if member.bill_code:
            return Response("BILL account must be deleted first", status=400)

        with LDAPAccountManager() as lm:
            try:
                lm.delete_account(member.username)
            except LDAPError as e:
                return Response(str(e), status=400)

        # Delete account information from user in db
        member.username = None
        member.save()

        return Response(status=200)


@api_view(['POST'])
def change_ldap_password(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    password = request.data.get('password')
    mailToUser = request.data.get('mail_to_user')
    if not password:
        return Response("password field missing", status=400)

    with LDAPAccountManager() as lm:
        try:
            lm.change_password(member.username, password)
            if mailToUser:
                status = mailNewPassword(member, password)
                if not status:
                    return Response("Password changed, failed to send mail", status=500)
        except LDAPError as e:
            return Response(str(e), status=400)

    return Response(status=200)


class BILLAccountView(APIView):
    def get(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if not member.bill_code:
            return Response("Member has no BILL account", status=400)

        bm = BILLAccountManager()
        try:
            result = bm.get_bill_info(member.bill_code)
        except BILLException as e:
            return Response(str(e), status=400)

        return Response(result, status=200)

    def post(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if member.bill_code:
            return Response("BILL account already exists", status=400)
        if not member.username:
            return Response("LDAP account missing", status=400)

        bm = BILLAccountManager()
        try:
            bill_code = bm.create_bill_account(member.username)
        except BILLException as e:
            return Response(str(e), status=400)

        member.bill_code = bill_code
        member.save()

        return Response(status=200)

    def delete(self, request, member_id):
        member = get_object_or_404(Member, id=member_id)

        if not member.bill_code:
            return Response("Member has no BILL account", status=400)

        bm = BILLAccountManager()
        try:
            bm.delete_bill_account(member.bill_code)
        except BILLException as e:
            return Response(str(e), status=400)

        member.bill_code = None
        member.save()

        return Response(status=200)


# JSON API:s

# Used by BILL
@api_view(['GET'])
def memberTypesForMember(request, mode, query):

    try:
        if mode == 'username':
            member = Member.objects.get(username=query)
        elif mode == 'studynumber':
            member = Member.objects.get(student_id=query)
        else:
            return Response(status=400)
    except Member.DoesNotExist as e:
        return Response(status=200)

    membertypes = {}

    for e in MemberType.objects.filter(member=member):
        membertypes[e.type] = (str(e.begin_date), str(e.end_date))

    data = {
        "given_names": member.given_names.split(),
        "surname": member.surname,
        "nickname": "",
        "preferred_name": member.preferred_name,
        "membertypes": membertypes
    }

    return Response(data, status=200)


# Used by GeneriKey
@api_view(['GET'])
def membersByMemberType(request, membertype, field=None):
    member_pks = MemberType.objects.filter(type=membertype, end_date=None).values_list("member", flat=True)
    fld = "username" if field == "usernames" else "student_id"
    members = Member.objects.filter(pk__in=member_pks).values_list(fld, flat=True)
    return Response(members, status=200)


# Data for HTK
# JSON file including all necessary information for HTK, i.e. member's activity at TF
@api_view(['GET'])
def htkDump(request, member_id=None):
    def dumpMember(member):
        # Functionaries
        funcs = Functionary.objects.filter(member=member)
        func_list = []
        for func in funcs:
            func_str = "{}: {} > {}".format(
                func.functionarytype.name,
                func.begin_date,
                func.end_date
            )
            func_list.append(func_str)
        # Groups
        groups = GroupMembership.objects.filter(member=member)
        group_list = []
        for group in groups:
            group_str = "{}: {} > {}".format(
                group.group.grouptype.name,
                group.group.begin_date,
                group.group.end_date
            )
            group_list.append(group_str)
        # Membertypes
        types = MemberType.objects.filter(member=member)
        type_list = []
        for type in types:
            type_str = "{}: {} > {}".format(
                type.get_type_display(),
                type.begin_date,
                type.end_date
            )
            type_list.append(type_str)
        # Decorations
        decorations = DecorationOwnership.objects.filter(member=member)
        decoration_list = []
        for decoration in decorations:
            decoration_str = "{}: {}".format(
                decoration.decoration.name,
                decoration.acquired
            )
            decoration_list.append(decoration_str)

        return {
            "id": member.id,
            "name": member.full_name,
            "functionaries": func_list,
            "groups": group_list,
            "membertypes": type_list,
            "decorations": decoration_list
        }

    if member_id:
        member = get_object_or_404(Member, id=member_id)
        data = dumpMember(member)
    else:
        data = [dumpMember(member) for member in Member.objects.all()]

    return Response(data, status=200, headers={'Content-Disposition': 'attachment; filename="HTKdump_{}.json"'.format(datetime.today().date())})


# CSV-render class
class ModulenRenderer(csv_renderer.CSVRenderer):
    header = ['name', 'street_address', 'postal_code', 'city', 'country']


# List of addresses whom to post modulen to
@api_view(['GET'])
@renderer_classes((ModulenRenderer,))
def modulenDump(request):

    recipients = Member.objects.exclude(
            postal_code='02150'
        ).exclude(
            dead=True
        ).filter(
            subscribed_to_modulen=True
        )

    recipients = [x for x in recipients if x.isValidMember()]

    content = [{
        'name': recipient._get_full_name(),
        'street_address': recipient.street_address,
        'postal_code': recipient.postal_code,
        'city': recipient.city,
        'country': recipient.country
        } for recipient in recipients]

    return Response(content, status=200, headers={'Content-Disposition': 'attachment; filename="modulendump_{}.csv"'.format(datetime.today().date())})


class ActiveRenderer(csv_renderer.CSVRenderer):
    header = ['position', 'member']


# Lists all members that are active at the moment. These are members
# that are either functionaries right now or in a group that has an
# active mandate
@api_view(['GET'])
@renderer_classes((ActiveRenderer,))
def activeDump(request):
    now = datetime.now().date()
    content = []

    # Functionaries
    all_functionaries = Functionary.objects.filter(
        begin_date__lt=now,
        end_date__gt=now
    )
    for func in all_functionaries:
        content.append({
            'position': str(func.functionarytype),
            'member': ''
        })
        content.append({
            'position': '',
            'member': func.member._get_full_preferred_name()
        })

    # Groups
    groupmemberships = GroupMembership.objects.all()
    grouped_by_group = defaultdict(list)
    for membership in groupmemberships:
        if membership.group.begin_date < now and membership.group.end_date > now:
            grouped_by_group[membership.group].append(membership.member)
    for group, members in grouped_by_group.items():
        content.append({
            'position': str(group.grouptype),
            'member': ''
        })
        content.extend([{
            'position': '',
            'member': m._get_full_preferred_name()
        } for m in members])

    return Response(content, status=200, headers={'Content-Disposition': 'attachment; filename="activedump.csv"'})


class FullRenderer(csv_renderer.CSVRenderer):
    header = ['id', 'given_names', 'preferred_name', 'surname', 'membertype',
    'street_address', 'postal_code', 'city', 'country', 'birth_date',
    'student_id', 'enrolment_year', 'graduated', 'graduated_year',
    'degree_programme', 'dead','phone', 'email', 'subscribed_to_modulen',
    'allow_publish_info', 'username', 'bill_code', 'comment', 'should_be_stalmed']


# "Fulldump". If you need some arbitrary bit of info this with some excel magic might do the trick.
# Preferably tough for all common needs implement a specific endpoint for it (like modulen or HTK)
# to save time in the long run.
@api_view(['GET'])
@renderer_classes((FullRenderer,))
def fullDump(request):

    members = Member.objects.exclude(dead=True)

    content = [{
        'id': member.id,
        'given_names': member.given_names,
        'preferred_name': member.preferred_name,
        'surname': member.surname,
        'membertype': str(member.getMostRecentMemberType()),
        'street_address': member.street_address,
        'postal_code': member.postal_code,
        'city': member.city,
        'country': member.country,
        'birth_date': member.birth_date,
        'student_id': member.student_id,
        'enrolment_year': member.enrolment_year,
        'graduated': member.graduated,
        'graduated_year': member.graduated_year,
        'degree_programme': member.degree_programme,
        'dead': member.dead,
        'phone': member.phone,
        'email': member.email,
        'subscribed_to_modulen': member.subscribed_to_modulen,
        'allow_publish_info': member.allow_publish_info,
        'username': member.username,
        'bill_code': member.bill_code,
        'comment': member.comment,
        'should_be_stalmed': member.shouldBeStalm()}
        for member in members]

    return Response(content, status=200, headers={'Content-Disposition': 'attachment; filename="fulldump_{}.csv"'.format(datetime.today().date())})
