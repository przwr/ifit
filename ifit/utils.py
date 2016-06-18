# -*- coding: utf-8 -*-
from ifit.models import Profile, FriendRequest


def add_friend(request, profile_id):
	me = Profile.objects.filter(user=request.user)
	friend = Profile.objects.filter(id=profile_id)
	if len(me) == 1 and len(friend) == 1:
		request = FriendRequest(request=me[0], friend=friend[0])
		request.save()
		me[0].friends_requests.add(request)
		me[0].save()
		friend[0].friends_requests.add(request)
		friend[0].save()


def remove_friend(request, profile_id):
	me = Profile.objects.filter(user=request.user)
	friend = Profile.objects.filter(id=profile_id)
	if len(me) == 1 and len(friend) == 1:
		me[0].friends.remove(friend[0])
		me[0].save()
		friend[0].friends.remove(me[0])
		friend[0].save()
