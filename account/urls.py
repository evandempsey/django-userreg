from django.conf.urls.defaults import patterns, url
from account.views import authenticateUser, deauthenticateUser, password, register, \
    requestRecovery, recover, activate, requestDeactivation, deactivate, manageAccount

urlpatterns = patterns(
    '',
    url(r'^login/$', authenticateUser),
    url(r'^logout/$', deauthenticateUser),
    url(r'^register/$', register),
    url(r'^recover/$', requestRecovery),
    url(r'^recover/(?P<username>\w+)/(?P<key>[a-z0-9]{64})/$', recover),
    url(r'^activate/(?P<username>\w+)/(?P<key>[a-z0-9]{64})/$', activate),
    url(r'^manage/$', manageAccount),
    url(r'^manage/password/$', password),
    url(r'^manage/deactivate/$', requestDeactivation),
    url(r'^manage/deactivate/(?P<username>\w+)/(?P<key>[a-z0-9]{64})/$', deactivate),

)
