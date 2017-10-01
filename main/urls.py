"""MINS main urls."""
from django.conf.urls import patterns, url


urlpatterns = patterns('main.views',
                       url(r'^$', 'dashboard', name='dashboard'),
                       url(r'^view/$', 'register'),
                       url(r'^certificate/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
                           'get_cert', name='get_cert'),
                       url(r'^mcic/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
                           'get_mcert', name='get_mcert'),
                       url(r'^eslip/(?P<id>\d+)/$', 'get_eslip',
                           name='get_eslip'),
                       url(r'^pvcoc/(?P<id>\d+)/$', 'get_pvcoc',
                           name='get_pvcoc'),
                       url(r'^report/(?P<id>\d+)/$', 'get_report',
                           name='get_report'),
                       url(r'^bond/(?P<id>\d+)/$', 'get_bond',
                           name='get_bond'),
                       url(r'^setup/$', 'edit_resetup', name='edit_setup'),
                       url(r'^epayment/$', 'epayment', name='epay'),
                       )
