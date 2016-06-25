# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse

from ifit.constants import WRONG_DATA
from ifit.models import Profile, FriendRequest


# TODO przerobić na ViewSets

# @require_http_methods(["POST"])
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
		return HttpResponse()
	else:
		return JsonResponse({'error': WRONG_DATA})


# @require_http_methods(["POST"])
def remove_friend(request, profile_id):
	me = Profile.objects.filter(user=request.user)
	friend = Profile.objects.filter(id=profile_id)
	if len(me) == 1 and len(friend) == 1:
		me[0].friends.remove(friend[0])
		me[0].save()
		friend[0].friends.remove(me[0])
		friend[0].save()
		return HttpResponse()
	else:
		return JsonResponse({'error': WRONG_DATA})


def add_to_challenge(request):
	if 'id' in request.GET and 'challenged' in request.GET:
		id = request.GET.get("id")
		challenged = request.GET.get("challenged")
		return JsonResponse({'r': request.GET['id']})
	return HttpResponse()
