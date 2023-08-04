from django.conf.urls import url, include
from rest_framework import routers
from api.views import *

class RootView(routers.APIRootView):
    name = 'Katalogen root API'
    description = ''

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.APIRootView = RootView
router.register(r'members', MemberViewSet)
router.register(r'grouptypes', GroupTypeViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'groupmemberships', GroupMembershipViewSet)
router.register(r'functionarytypes', FunctionaryTypeViewSet)
router.register(r'functionaries', FunctionaryViewSet)
router.register(r'decorations', DecorationViewSet)
router.register(r'decorationownerships', DecorationOwnershipViewSet)
router.register(r'membertypes', MemberTypeViewSet)
router.register(r'applicants', ApplicantViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^multi-groupmemberships/$', multi_group_memberships_save),
    url(r'^multi-functionaries/$', multi_functionaries_save),
    url(r'^multi-decorationownerships/$', multi_decoration_ownerships_save),
    url(r'^multi-applicantsubmissions/$', multi_applicant_submissions, name='multi_applicant_submissions'),
    url(r'^accounts/ldap/(\d+)/$', LDAPAccountView.as_view()),
    url(r'^accounts/ldap/change_pw/(\d+)/$', change_ldap_password),
    url(r'^accounts/bill/(\d+)/$', BILLAccountView.as_view()),
    url(r'^applicants/make-member/(\d+)/$', ApplicantMembershipView.as_view()),
    url(r'^dump-htk/(\d+)?$', dump_htk, name='dump_htk'),
    url(r'^dump-modulen/$', dump_modulen, name='dump_modulen'),
    url(r'^dump-active/$', dump_active, name='dump_active'),
    url(r'^dump-arsk/$', dump_arsk, name='dump_arsk'),
    url(r'^dump-regemails/$', dump_reg_emails, name='dump_reg_emails'),
    url(r'^dump-studentbladet/$', dump_studentbladet, name='dump_studentbladet'),
    # Used by BILL
    url(r'^memberTypesForMember/(?P<mode>username|studynumber)/(?P<query>[A-Za-z0-9]+)/$', member_types_for_member),
    # Used by Generikey
    url(r'^membersByMemberType/([A-Z]{2})/(\w+)?$', members_by_member_type),
]
