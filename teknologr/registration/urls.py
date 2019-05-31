from django.conf.urls import url, include
from registration.views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='registration.views.home'),
    url(r'^submit/$', SubmitView.as_view(), name='registration.views.submit'),
    # TODO: done url?
    # TODO: error url?
]
