"""MINS payment urls."""
from django.conf.urls import patterns, url


urlpatterns = patterns('reports.views',
                       url(r'^$', 'reports', name='reports'),
                       url(r'^insurance/$', 'insurance', name='insurance'),
                       url(r'^agency/$', 'agency', name='agency'),
                       url(r'^akiira/$', 'regulator', name='regulator'),
                       url(r'^aibk/$', 'regulator', name='regulator'),
                       url(r'^krakebs/$', 'krakebs', name='krakebs'),)
