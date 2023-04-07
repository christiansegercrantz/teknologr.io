from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count

from members.models import *
from members.forms import *
from members.programmes import DEGREE_PROGRAMME_CHOICES
from registration.models import Applicant
from registration.forms import RegistrationForm


def set_side_context(context, category, active_obj=None):
    side = {}
    side['active'] = category
    side['active_obj'] = active_obj
    side['new_button'] = True
    if category == 'members':
        side['sname'] = 'medlem'
        side['form'] = MemberForm(initial={'given_names': '', 'surname': ''}, auto_id="mmodal_%s")
        objects = Member.objects.order_by('-modified')[:50]
        if active_obj:
            active = Member.objects.get(pk=active_obj)
            if active not in objects:
                from itertools import chain
                objects = list(chain([active], objects))
        side['objects'] = objects
    elif category == 'groups':
        side['sname'] = 'grupp'
        side['form'] = GroupTypeForm(auto_id="gtmodal_%s")
        side['objects'] = GroupType.objects.annotate(count=Count('groups', distinct=True))
    elif category == 'functionaries':
        side['sname'] = 'post'
        side['form'] = FunctionaryTypeForm(auto_id="ftmodal_%s")
        side['objects'] = FunctionaryType.objects.annotate(count=Count('functionaries', distinct=True))
    elif category == 'decorations':
        side['sname'] = 'betygelse'
        side['form'] = DecorationForm(auto_id="dmodal_%s")
        side['objects'] = Decoration.objects.annotate(count=Count('ownerships', distinct=True))
    elif category == 'applicants':
        side['sname'] = 'ansökning'
        side['objects'] = Applicant.objects.all()
        side['new_button'] = False
        side['applicant_tool_icons'] = True
        side['multiple_applicants_form'] = MultipleApplicantAdditionForm()

    context['side'] = side


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def empty(request, category):
    context = {}
    set_side_context(context, category)
    return render(request, 'base.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def member(request, member_id):
    context = {}

    member = get_object_or_404(Member, id=member_id)
    context['member'] = member

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            from ldap import LDAPError
            try:
                form.save()
            except LDAPError:
                form.add_error("email", "Could not sync to LDAP")
            context['result'] = 'success'
        else:
            context['result'] = 'failure'
    else:
        form = MemberForm(instance=member)

    context['programmes'] = [
            programme
            for school, programmes in DEGREE_PROGRAMME_CHOICES.items()
            for programme in programmes
    ]
    context['programmes'].sort()

    context['form'] = form
    context['full_name'] = member

    # Get decorations
    context['decoration_ownerships'] = DecorationOwnership.objects.filter(member__id=member_id).order_by('-acquired')
    context['add_do_form'] = DecorationOwnershipForm(initial={'member': member_id})

    # Get functionary positions
    context['functionaries'] = Functionary.objects.filter(member__id=member_id).order_by('-begin_date')
    context['add_f_form'] = FunctionaryForm(initial={'member': member_id})

    # Get groups
    context['group_memberships'] = GroupMembership.objects.filter(member__id=member_id).order_by('-group__begin_date')
    context['add_gm_form'] = GroupMembershipForm(initial={'member': member_id})

    # Get membertypes
    context['membertypes'] = MemberType.objects.filter(member__id=member_id)
    context['add_mt_form'] = MemberTypeForm(initial={'member': member_id})

    # Get user account info
    from api.ldap import LDAPAccountManager
    from api.bill import BILLAccountManager, BILLException
    if member.username:
        try:
            with LDAPAccountManager() as lm:
                context['LDAP'] = {'groups': lm.get_ldap_groups(member.username)}
        except Exception:
            context['LDAP'] = "error"

    if member.bill_code:
        bm = BILLAccountManager()
        try:
            context['BILL'] = bm.get_bill_info(member.bill_code)
        except BILLException as e:
            context['BILL'] = {"error": str(e)}

    # load side list items
    set_side_context(context, 'members', member.id)
    return render(request, 'member.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def membertype_form(request, membertype_id):
    membertype = get_object_or_404(MemberType, id=membertype_id)
    form = MemberTypeForm(instance=membertype)
    context = {'form': form, 'formid': 'edit-mt-form'}
    return render(request, 'membertypeform.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def group(request, grouptype_id, group_id=None):
    context = {}

    grouptype = get_object_or_404(GroupType, id=grouptype_id)
    context['grouptype'] = grouptype

    form = GroupTypeForm(instance=grouptype)

    # Get groups of group type
    context['groups'] = Group.objects.filter(grouptype__id=grouptype_id).annotate(num_members=Count('memberships', distinct=True)).order_by('-begin_date')
    context['edit_gt_form'] = form

    context['add_g_form'] = GroupForm(initial={"grouptype": grouptype_id})

    if group_id is not None:
        group = get_object_or_404(Group, id=group_id)
        context['group'] = group
        context['edit_g_form'] = GroupForm(instance=group)
        context['add_gm_form'] = GroupMembershipForm(initial={"group": group_id})
        context['groupmembers'] = GroupMembership.objects.filter(group=group).order_by('member__surname', 'member__given_names')
        context['emails'] = "\n".join(
            [membership.member.email for membership in context['groupmembers']]
        )

    set_side_context(context, 'groups', grouptype.id)
    return render(request, 'group.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def functionary_type(request, functionarytype_id):
    context = {}

    functionarytype = get_object_or_404(FunctionaryType, id=functionarytype_id)
    context['functionaryType'] = functionarytype
    form = FunctionaryTypeForm(instance=functionarytype)

    # Get functionaries of functionary type
    context['functionaries'] = Functionary.objects.filter(
        functionarytype__id=functionarytype_id).order_by('-begin_date', 'member__surname', 'member__given_names')
    context['edit_ft_form'] = form
    context['add_f_form'] = FunctionaryForm(initial={"functionarytype": functionarytype_id})

    set_side_context(context, 'functionaries', functionarytype.id)
    return render(request, 'functionary.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def decoration(request, decoration_id):
    context = {}

    decoration = get_object_or_404(Decoration, id=decoration_id)
    context['decoration'] = decoration
    context['edit_d_form'] = DecorationForm(instance=decoration)

    # Get groups of group type
    context['decorations'] = DecorationOwnership.objects.filter(decoration__id=decoration_id).order_by('-acquired', 'member__surname', 'member__given_names')
    context['add_do_form'] = DecorationOwnershipForm(initial={"decoration": decoration_id})

    set_side_context(context, 'decorations', decoration.id)
    return render(request, 'decoration.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login')
def applicant(request, applicant_id):
    context = {}

    applicant = get_object_or_404(Applicant, id=applicant_id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
    else:
        form = RegistrationForm(instance=applicant)

    context['applicant'] = applicant
    context['form'] = form
    context['make_member_form'] = ApplicantAdditionForm()

    set_side_context(context, 'applicants', applicant.id)
    return render(request, 'applicant.html', context)
