from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='katalogen.views.home'),
    url(r'^search$', views.search, name='katalogen.views.search'),
    url(r'^([A-ZÅÄÖ])$', views.startswith, name='katalogen.views.startswith'),
    url(r'^person/(\d)$', views.profile, name='katalogen.views.profile'),
    url(r'^profile$', views.myprofile, name='katalogen.views.myprofile'),
]
