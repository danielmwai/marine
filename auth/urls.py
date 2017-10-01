"""MINS auth urls."""
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'auth.views',
    url(r'^$', 'profile', name='profile'),)
