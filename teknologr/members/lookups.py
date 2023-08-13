from ajax_select import register, LookupChannel
from members.models import Member
from registration.models import Applicant
from api.utils import findMembers, findApplicants


@register('member')
class MemberLookup(LookupChannel):
    model = Member

    def get_query(self, q, request):
        members = findMembers(q)
        return members

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.full_name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return obj.get_full_name_HTML()

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return obj.full_name


@register('applicant')
class ApplicantLookup(LookupChannel):
    model = Applicant

    def get_query(self, q, request):
        return findApplicants(q)

    def get_result(self, obj):
        return obj.full_name

    def format_match(self, obj):
        return obj.full_name

    def format_item_display(self, obj):
        return obj.full_name
