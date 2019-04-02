from django.conf.urls import url, include
from registration.views import *

urlpatterns = [
    url(r'^$', home, name='registration.views.home'),
    # TODO: submit url?
    # TODO: done url?
    # TODO: error url?
]
