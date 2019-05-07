from django.conf.urls import url, include
from registration.views import *

urlpatterns = [
    url(r'^$', home, name='registration.views.home'),
    url(r'^submit/$', submit, name='registration.views.submit'),
    # TODO: done url?
    # TODO: error url?
]
