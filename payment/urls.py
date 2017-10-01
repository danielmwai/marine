"""MINS payment urls."""
from django.conf.urls import patterns, url


urlpatterns = patterns('payment.views',
                       url(r'^$', 'payments', name='payments'),
                       url(r'^apex/$', 'payments'),
                       url(r'^kenswitch/$', 'kenpay', name='kenpay'),)
