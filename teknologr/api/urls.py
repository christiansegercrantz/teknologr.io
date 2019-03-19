from django.conf.urls import url, include
from rest_framework import routers
from api.views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'members', MemberViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'groupTypes', GroupTypeViewSet)
router.register(r'groupMembership', GroupMembershipViewSet)
router.register(r'functionaries', FunctionaryViewSet)
router.register(r'functionaryTypes', FunctionaryTypeViewSet)
router.register(r'decorations', DecorationViewSet)
router.register(r'decorationOwnership', DecorationOwnershipViewSet)
router.register(r'memberTypes', MemberTypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^multiGroupMembership/$', memberListSave),
    url(r'^memberTypesForMember/(?P<mode>username|studynumber)/(?P<query>[A-Za-z0-9]+)/$', memberTypesForMember),
    url(r'^accounts/ldap/(\d+)/$', LDAPAccountView.as_view()),
    url(r'^accounts/ldap/change_pw/(\d+)/$', change_ldap_password),
    url(r'^accounts/bill/(\d+)/$', BILLAccountView.as_view()),
    url(r'^htkdump/(\d+)?$', htkDump, name='api.views.htkDump'),
    url(r'^modulendump/$', modulenDump, name='api.views.modulenDump'),
    url(r'^fulldump/$', fullDump, name='api.views.fullDump'),
    url(r'^activedump/$', activeDump, name='api.views.activeDump'),
    url(r'^arskdump/$', arskDump, name='api.views.arskDump'),
    url(r'^membersByMemberType/([A-Z]{2})/(\w+)?$', membersByMemberType)
]
