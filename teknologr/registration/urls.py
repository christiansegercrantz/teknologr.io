from django.conf.urls import url, include
from registration.views import *

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^submit/$', SubmitView.as_view(), name='submit'),
]
