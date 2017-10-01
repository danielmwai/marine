"""marine URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main import urls as main_urls
from forms import urls as forms_urls
from payment import urls as pay_urls
from auth import urls as auth_urls
from reports import urls as report_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.dashboard', name='home'),
    url(r'^dashboard/', include(main_urls)),
    url(r'^forms/', include(forms_urls)),
    url(r'^logout/$', 'auth.views.log_out', name='logout'),
    url(r'^login/$', 'auth.views.log_in', name='login'),
    url(r'^account/$', 'auth.views.account', name='account'),
    url(r'^register/$', 'auth.views.register', name='register'),
    url(r'^register/(?P<id>\d+)/$', 'auth.views.registration',
        name='registration'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^verify/$', 'main.views.verify', name='verify'),
    url(r'^quotation/$', 'main.views.quote', name='quote'),
    url(r'^payment/$', 'main.views.payment', name='payment'),
    url(r'^payments/', include(pay_urls)),
    url(r'^reports/', include(report_urls)),
    url(r'^accounts/', include(auth_urls)),
    url(r'^schedule/$', 'main.views.schedule', name='schedule'),
    url(r'^certificate/$', 'main.views.cert_verify', name='cverify'),
    url(r'^schedule/setup/$', 'main.views.re_setup', name='re_setup'),
    url(r'^schedule/edit/$', 'main.views.edit_schedule',
        name='edit_schedule'),
]

handler400 = 'main.views.handler_400'
handler404 = 'main.views.handler_404'
handler500 = 'main.views.handler_500'

admin.site.site_header = 'Marine Insurance Administration'
admin.site.site_title = 'Marine Insurance administration'
admin.site.index_title = 'Marine Insurance admin'
