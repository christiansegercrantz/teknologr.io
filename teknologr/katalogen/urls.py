from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='katalogen.views.home'),
    url(r'^search$', views.search, name='katalogen.views.search'),
    url(r'^([A-ZÅÄÖ])$', views.startswith, name='katalogen.views.startswith'),
    url(r'^person/(\d+)$', views.profile, name='katalogen.views.profile'),
    url(r'^profile$', views.myprofile, name='katalogen.views.myprofile'),
    url(r'^decorations$', views.decorations, name='katalogen.views.decorations'),
    url(r'^decorations/(\d+)$', views.decoration_ownerships, name='katalogen.views.decoration_ownerships'),
    url(r'^functionaries$', views.functionary_types, name='katalogen.views.functionary_types'),
    url(r'^functionaries/(\d+)$', views.functionaries, name='katalogen.views.functionaries'),
    url(r'^groups$', views.group_types, name='katalogen.views.group_types'),
    url(r'^groups/(\d+)$', views.groups, name='katalogen.views.groups'),
]
