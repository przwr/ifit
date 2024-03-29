# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from ifit.utils import *
from ifit.views import *

# import ifit.signals ma tu być, bo inaczej nie będą działać sygnały!
import ifit.signals

admin.autodiscover()

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', index, name='index'),
	# LOGIN / LOGOUT for testing from Browser
	url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
	# LOGIN AND REGISTRATION
	url(r'^api/rest-auth/', include('rest_auth.urls')),
	url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
	url(r'^api/account/', include('allauth.urls')),
	# this url is used to generate email content
	url(r'^api/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
	    TemplateView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),

	# MODELS
	url(r'^api/user/$', UsersList.as_view(), name='users'),
	url(r'^api/user/(?P<pk>[0-9]+)$', UserDetail.as_view(), name='user'),
	url(r'^api/group/$', GroupsList.as_view(), name='groups'),
	url(r'^api/group/(?P<pk>[0-9]+)$', GroupDetail.as_view(), name='group'),
	url(r'^api/challenge/$', ChallengeList.as_view(), name='challenges'),
	url(r'^api/challenge/(?P<pk>[0-9]+)$', ChallengeDetail.as_view(), name='challenge'),
	url(r'^api/challenge_data/$', ChallengeDataList.as_view(), name='challenge_data'),
	url(r'^api/challenge_data/(?P<pk>[0-9]+)$', ChallengeDataDetail.as_view(), name='challenge_data'),
	url(r'^api/profile/$', ProfilesList.as_view(), name='profiles'),
	url(r'^api/profile/(?P<pk>[0-9]+)$', ProfileDetail.as_view(), name='profile'),
	url(r'^api/friend_request/$', FriendRequestList.as_view(), name='friend_request'),
	url(r'^api/friend_request/(?P<pk>[0-9]+)$', FriendRequestDetail.as_view(), name='friend_request'),

	# FUNCTIONS
	url(r'^api/add_friend/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view({'post': 'add_friend'}), name='add_friend'),
	url(r'^api/accept_friend/(?P<pk>[0-9]+)/$', FriendRequestViewSet.as_view({'post': 'accept_friend'}),
	    name='accept_friend'),
	url(r'^api/reject_friend/(?P<pk>[0-9]+)/$', FriendRequestViewSet.as_view({'post': 'reject_friend'}),
	    name='reject_friend'),
	url(r'^api/search_profile/$', ProfileViewSet.as_view({'get': 'search_profile'}), name='search_profile'),

	url(r'^api/get_challenged/(?P<pk>[0-9]+)$', ChallengeViewSet.as_view({'get': 'get_challenged'}),
	    name='get_challenged'),
	url(r'^api/remove_friend/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view({'post': 'remove_friend'}),
	    name='remove_friend'),
	url(r'^api/add_to_challenge/(?P<pk>[0-9]+)/$', ChallengeViewSet.as_view({'post': 'add_to_challenge'}),
	    name='add_to_challenge'),
	url(r'^api/remove_from_challenge/(?P<pk>[0-9]+)/$', ChallengeDataViewSet.as_view({'post': 'remove_from_challenge'}),
	    name='remove_from_challenge'),
	url(r'^api/challenge_response/(?P<pk>[0-9]+)/$', ChallengeDataViewSet.as_view({'post': 'challenge_response'}),
	    name='challenge_response'),
	url(r'^api/set_challenge_result/(?P<pk>[0-9]+)/$', ChallengeDataViewSet.as_view({'post': 'set_challenge_result'}),
	    name='set_challenge_result'),
	url(r'^api/set_all_challenges_result/(?P<pk>[0-9]+)/$',
	    ChallengeViewSet.as_view({'post': 'set_all_challenges_result'}),
	    name='set_all_challenges_result'),

	url(r'^api/upload_avatar/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view({'post': 'upload_avatar'}),
	    name='upload_avatar'),
	url(r'^api/get_avatar/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view({'get': 'get_avatar'}),
	    name='get_avatar'),
]
