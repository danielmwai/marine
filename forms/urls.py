"""MINS forms urls."""
from django.conf.urls import patterns, url


urlpatterns = patterns('forms.views',
                       url(r'^$', 'search', name='forms_search'),
                       url(r'^register/$', 'register', name='registration'),
                       url(r'^cargo/$', 'cargo', name='cargo'),
                       url(r'^cargo/(?P<id>[0-9A-Za-z_\-{32}\Z]+)/$',
                           'edit_cargo', name='edit_cargo'),
                       url(r'^bonds/$', 'bonds', name='bonds'),
                       url(r'^bonds/new/$', 'new_bonds', name='new_bonds'),
                       url(r'^bonds/validate/(?P<id>\d+)/$', 'validate_bonds',
                           name='validate_bonds'),
                       url(r'^public/$', 'public_search',
                           name='public_search'),
                       url(r'^premiums/$', 'premiums', name='premiums'),
                       url(r'^registrations/$', 'registrations', name='regs'),
                       url(r'^registrations/(?P<id>\d+)/$', 'reg_validate',
                           name='regv'),
                       url(r'^registration/$', 'new_user', name='new_user'),
                       url(r'^client/$', 'new_client', name='new_client'),
                       url(r'^cbm/$', 'cbm_calculator', name='cbm_calc'),
                       url(r'^claims/(?P<id>\d+)/$', 'claims', name='claims'),
                       url(r'^csform/(?P<id>\d+)/$', 'csform', name='csform'),
                       )
