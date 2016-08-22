# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ifit.constants import DECLINED, FAILED, ACCEPTED, DONE
from ifit.permissions import *
from ifit.serializers import *


def index(request):
	return HttpResponse("To jest serwer aplikacji Challenge4U")


class UsersList(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (IsThisUserOrSuperUser,)

	def get_queryset(self):
		user = self.request.user
		if not isinstance(user, AnonymousUser):
			return User.objects.filter(id=user.id)
		raise PermissionDenied


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsThisUserOrSuperUser,)


class GroupsList(generics.ListCreateAPIView):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = (IsOwnerOrReadOnly,)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = (IsOwnerOrReadOnly,)


class ChallengeList(generics.ListCreateAPIView):
	serializer_class = ChallengeSerializer
	permission_classes = (IsOwner,)

	def get_queryset(self):
		user = self.request.user
		if isinstance(user, AnonymousUser):
			raise PermissionDenied
		return Challenge.objects.filter(owner=user.profile)


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Challenge.objects.all()
	serializer_class = ChallengeSerializer


class ChallengeDataList(generics.ListAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	permission_classes = (IsChallenged,)

	def get_queryset(self):
		user = self.request.user
		if isinstance(user, AnonymousUser):
			raise PermissionDenied
		return ChallengeData.objects.filter(challenged=user.profile)


class ChallengeDataDetail(generics.RetrieveAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	permission_classes = (IsChallengedOrOwner,)


class ProfilesList(generics.ListCreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

	def get_queryset(self):
		user = self.request.user
		if not isinstance(user, AnonymousUser):
			return Profile.objects.filter(user=user)
		raise PermissionDenied


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class FriendRequestList(generics.ListCreateAPIView):
	queryset = FriendRequest.objects.all()
	serializer_class = FriendRequestSerializer

	def get_queryset(self):
		user = self.request.user
		profile = user.profile
		if not isinstance(user, AnonymousUser):
			return FriendRequest.objects.filter(Q(requester=profile) | Q(friend=profile))
		raise PermissionDenied


class FriendRequestDetail(generics.RetrieveAPIView):
	queryset = FriendRequest.objects.all()
	serializer_class = FriendRequestSerializer


class ChallengeViewSet(ModelViewSet):
	queryset = Challenge.objects.all()
	serializer_class = ChallengeSerializer

	@detail_route(methods=['GET'])
	def get_challenged(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge = self.get_object()
			challenge_data = ChallengeData.objects.filter(challenge=challenge)
			challenged = [
				{'username': ch.challenged.username, 'id': ch.id, 'profile': ch.challenged.id,
				 'avatar': ch.challenged.get_avatar, 'state': ch.state}
				for ch in challenge_data]
			return JsonResponse(list(challenged), safe=False)
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def add_to_challenge(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge = self.get_object()
			me = request.user.profile
			if 'challenged' in request.POST:
				challenged = request.POST["challenged"]
				challenged_array = []
				for c in challenged.split('_'):
					if c.isdigit():
						challenged_array.append(c)
				challenge_data = ChallengeData.objects.filter(challenge=challenge).values_list('challenged__id',
				                                                                               flat=True)
				# friends = me.friends.all().values_list('id', flat=True)
				# profiles = Profile.objects.filter(Q(id__in=challenged) & Q(id__in=friends)).exclude(
				# 	id__in=challenge_data)

				profiles = Profile.objects.filter(id__in=challenged_array).exclude(id=me.id).exclude(
					id__in=challenge_data)
				added = []
				for profile in profiles:
					new_challenge_data = ChallengeData(challenger=me, challenge=challenge, challenged=profile)
					new_challenge_data.save()
					added.append(profile.id)
				return JsonResponse({'added': added})
			else:
				return JsonResponse({'error': 'Missing parameter <challenged>'})
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def set_all_challenges_result(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge = self.get_object()
			set_count = 0
			if not request.user.profile:
				raise PermissionDenied
			if 'state' in request.POST:
				state = request.POST["state"] == "True"
				challenge_datas = ChallengeData.objects.filter(challenge=challenge, challenger=request.user.profile)
				for challenge_data in challenge_datas:
					if challenge_data.state == ACCEPTED:
						if state:
							challenge_data.state = DONE
							challenge_data.save()
						else:
							challenge_data.state = FAILED
							challenge_data.save()
						set_count += 1
				return JsonResponse({'set_count': set_count})
			else:
				return JsonResponse({'error': 'Missing parameter <state>'})
		raise PermissionDenied


class ChallengeDataViewSet(ModelViewSet):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer

	@detail_route(methods=['POST'])
	def challenge_response(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge_data = self.get_object()
			if not request.user.profile or challenge_data.challenged != request.user.profile:
				raise PermissionDenied
			if 'state' in request.POST:
				state = request.POST["state"] == "True"
				if challenge_data.state == RECEIVED:
					if state:
						challenge_data.state = ACCEPTED
						challenge_data.save()
						return JsonResponse({'changed': 'Yes'})
					else:
						challenge_data.state = DECLINED
						challenge_data.save()
						return JsonResponse({'changed': 'Yes'})
				if challenge_data.state == ACCEPTED:
					if not state:
						challenge_data.state = FAILED
						challenge_data.save()
						return JsonResponse({'changed': 'Yes'})
					else:
						return JsonResponse({'changed': 'No'})
				else:
					return JsonResponse({'changed': 'No'})
			else:
				return JsonResponse({'error': 'Missing parameter <state>'})
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def remove_from_challenge(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge_data = self.get_object()
			if not request.user.profile or challenge_data.challenger != request.user.profile:
				raise PermissionDenied
			challenge_data.delete()
			return Response({'status': 'Ok'}, status=status.HTTP_200_OK)
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def set_challenge_result(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			challenge_data = self.get_object()
			if not request.user.profile or challenge_data.challenger != request.user.profile:
				raise PermissionDenied
			if 'state' in request.POST:
				state = request.POST["state"] == "True"
				if challenge_data.state == ACCEPTED:
					if state:
						challenge_data.state = DONE
						challenge_data.save()
						return JsonResponse({'set': 'Yes'})
					else:
						challenge_data.state = FAILED
						challenge_data.save()
						return JsonResponse({'set': 'Yes'})
				else:
					return JsonResponse({'set': 'No'})
			else:
				return JsonResponse({'error': 'Missing parameter <state>'})
		raise PermissionDenied


class ProfileViewSet(ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

	@detail_route(methods=['POST'])
	def add_friend(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			friend = self.get_object()
			me = request.user.profile
			if me and friend:
				req = FriendRequest(request=me, friend=friend)
				req.save()
				me.friends_requests.add(req)
				me.save()
				friend.friends_requests.add(req)
				friend.save()
				return HttpResponse()
			else:
				return JsonResponse({'error': 'Wrong data!'})
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def remove_friend(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			friend = self.get_object()
			me = request.user.profile
			if me and friend:
				me.friends.remove(friend)
				me.save()
				friend.friends.remove(me)
				friend.save()
				return HttpResponse()
			else:
				return JsonResponse({'error': 'Wrong data!'})
		raise PermissionDenied

	@detail_route(methods=['GET'])
	def search_profile(self, request):
		if not isinstance(request.user, AnonymousUser):
			if not request.user.profile:
				raise PermissionDenied
			if 'phrase' in request.GET:
				phrase = request.GET["phrase"]
				result = self.queryset.filter(user__username__startswith=phrase).exclude(id=request.user.profile.id)
				# TODO po wspólnych znajomych
				found = [{'username': profile.user.username, 'id': profile.id, 'avatar': profile.get_avatar}
				         for profile in result]
				return JsonResponse({'found': list(found)})
			else:
				return JsonResponse({'error': 'Missing parameter <phrase>'})
		raise PermissionDenied

	# TODO zrobić wrzucanie avatara
	@detail_route(methods=['POST'])
	def upload_avatar(self, request):
		if not isinstance(request.user, AnonymousUser):
			if not request.user.profile:
				raise PermissionDenied
			if 'image' in request.GET:
				image = request.GET["image"]
				return JsonResponse({'status': "Ok"})
			else:
				return JsonResponse({'error': 'Missing parameter <image>'})
		raise PermissionDenied


class FriendRequestViewSet(ModelViewSet):
	queryset = FriendRequest.objects.all()
	serializer_class = FriendRequestSerializer

	@detail_route(methods=['POST'])
	def accept_friend(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			req = self.get_object()
			me = request.user.profile
			if me and req.friend == me:
				friend = req.requester
				friend.friends.add(me)
				me.friends.add(friend)
				me.save()
				friend.save()
				req.delete()
				return JsonResponse({})
			else:
				return JsonResponse({'error': 'Not Your friend request!'})
		raise PermissionDenied

	@detail_route(methods=['POST'])
	def reject_friend(self, request, pk):
		if not isinstance(request.user, AnonymousUser):
			req = self.get_object()
			me = request.user.profile
			if me and req.friend == me:
				req.delete()
				return JsonResponse({})
			else:
				return JsonResponse({'error': 'Not Your friend request!'})
		raise PermissionDenied
