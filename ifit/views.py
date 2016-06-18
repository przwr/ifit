# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from ifit.permissions import *
from ifit.serializers import *


def index(request):
	return HttpResponse("To jest serwer aplikacji IF IT Challenge")


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


class ChallengesList(generics.ListCreateAPIView):
	serializer_class = ChallengeSerializer
	permission_classes = (IsOwner,)

	def get_queryset(self):
		user = self.request.user
		if isinstance(user, AnonymousUser):
			raise PermissionDenied
		return Challenge.objects.filter(owner=user)


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Challenge.objects.all()
	serializer_class = ChallengeSerializer
	permission_classes = (IsOwner,)


class ChallengeDataList(generics.ListCreateAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	permission_classes = (IsUser,)

	def get_queryset(self):
		user = self.request.user
		if isinstance(user, AnonymousUser):
			raise PermissionDenied
		return ChallengeData.objects.filter(user=user)


class ChallengeDataDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	permission_classes = (IsUser,)


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


class ChallengeDataDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	permission_classes = (IsUser,)


class FriendRequestList(generics.ListCreateAPIView):
	queryset = FriendRequest.objects.all()
	serializer_class = FriendRequestSerializer

	def get_queryset(self):
		user = self.request.user
		if not isinstance(user, AnonymousUser):
			return FriendRequest.objects.filter(Q(requester=user) | Q(friend=user))
		raise PermissionDenied


class FriendRequestDetail(generics.RetrieveAPIView):
	queryset = FriendRequest.objects.all()
	serializer_class = FriendRequestSerializer
