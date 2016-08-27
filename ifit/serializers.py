from django.contrib.auth.models import Group
from ifit.models import *


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('id', 'name',)


class FriendRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = FriendRequest
		fields = ('id', 'requester', 'friend')


class ProfileSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField()

	class Meta:
		model = Profile
		fields = ('id', 'user', 'username', 'friends', 'friends_requests', 'challenges', 'points', 'avatar')


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
		fields = ('id', 'challenged', 'challenge', 'state')

	# link = serializers.SerializerMethodField()
	#
	# def get_link(self, obj):
	# 	return "http://wrobelprzemek.com/app/api/" + (self.Meta.model.__name__).lower() + "/" + str(obj.id) + "/"


class ImageSerializer(serializers.ModelSerializer):
	image = Base64ImageField(max_length=None, use_url=True)

	class Meta:
		model = ImageFile
		fields = ("id", 'added')
