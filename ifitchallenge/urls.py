# -*- coding: utf-8 -*-
"""ifitchallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from rest_framework import routers

from ifit.views import *

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', index, name='index'),
	url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/user/$', UsersList.as_view(), name='users'),
	url(r'^api/user/(?P<pk>[0-9]+)$', UserDetail.as_view(), name='user'),
	url(r'^api/group/$', GroupsList.as_view(), name='groups'),
	url(r'^api/group/(?P<pk>[0-9]+)$', GroupDetail.as_view(), name='group'),
	url(r'^api/challenge/$', ChallengesList.as_view(), name='challenges'),
	url(r'^api/challenge/(?P<pk>[0-9]+)$', ChallengeDetail.as_view(), name='challenge'),
	url(r'^api/profile/$', ProfilesList.as_view(), name='profiles'),
	url(r'^api/profile/(?P<pk>[0-9]+)$', ProfileDetail.as_view(), name='profile'),

	# LOGIN AND REGISTRATION

	# this url is used to generate email content
	url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    TemplateView.as_view(template_name="password_reset_confirm.html"),
	    name='password_reset_confirm'),

	url(r'^api/rest-auth/', include('rest_auth.urls')),
	url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
	url(r'^api/account/', include('allauth.urls')),
	# url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),
]
