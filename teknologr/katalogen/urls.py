from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', 'katalogen.views.home'),
    url(r'^search$', 'katalogen.views.search'),
    url(r'^([A-ZÅÄÖ])$', 'katalogen.views.startswith'),
    url(r'^person/(\d)$', 'katalogen.views.profile'),
]