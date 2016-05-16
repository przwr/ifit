# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from ifit.serializers import *

from ifit.permissions import *


def index(request):
	return HttpResponse("To jest serwer aplikacji IF IT Challenge")


class UsersList(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (IsThisUserOrSuperUser,)

	def get_queryset(self):
		user = self.request.user
		if not isinstance(user, AnonymousUser):
			if user.is_superuser:
				return User.objects.all()
			else:
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
# permission_classes = (IsOwner,)

# def get_queryset(self):
# 	user = self.request.user
# 	if isinstance(user, AnonymousUser):
# 		raise PermissionDenied
# 	return Challenge.objects.filter(owner=user)


class ChallengeDataDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = ChallengeData.objects.all()
	serializer_class = ChallengeDataSerializer
	# permission_classes = (IsOwner,)


class ProfilesList(generics.ListCreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
