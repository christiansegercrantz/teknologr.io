from django.conf.urls import url, include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/members/'), name='home'),
    url(r'^(members|groups|functionaries|decorations|applicants)/$', views.empty, name='empty'),
    url(r'^members/(\d+)/$', views.member, name='member'),
    url(r'^membertype/(\d+)/form/$', views.membertype_form),
    url(r'^groups/(\d+)/$', views.group, name='group_type'),
    url(r'^groups/(\d+)/(\d+)/$', views.group, name='group'),
    url(r'^functionaries/(\d+)/$', views.functionary_type, name='functionary_type'),
    url(r'^decorations/(\d+)/$', views.decoration, name='decoration'),
    url(r'^applicants/(\d+)/$', views.applicant, name='applicant'),
]
