from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ifit.models import *


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name',)


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('id', 'user', 'friends', 'challenges', 'points', 'avatar')


class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'groups', 'profile')


class ChallengeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Challenge
		fields = ('id', 'name', 'category', 'value', 'description', 'begin', 'end', 'owner')


class ChallengeDataSerializer(serializers.ModelSerializer):
	challenge = ChallengeSerializer()

	class Meta:
		model = ChallengeData
		fields = ('id', 'user', 'challenge', 'state')

	# link = serializers.SerializerMethodField()
	#
	# def get_link(self, obj):
	# 	return "http://wrobelprzemek.com/app/api/" + (self.Meta.model.__name__).lower() + "/" + str(obj.id) + "/"
