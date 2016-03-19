from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ifit.models import *


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'groups',)


class ChallengeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Challenge
		fields = ('id', 'title', 'description', 'value',)

	# link = serializers.SerializerMethodField()
	#
	# def get_link(self, obj):
	# 	return "http://wrobelprzemek.com/app/api/" + (self.Meta.model.__name__).lower() + "/" + str(obj.id) + "/"
