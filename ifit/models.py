# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ifit.constants import CATEGORIES, RECEIVED, STATES
from django.contrib.auth.models import User
from rest_framework import serializers


class FriendRequest(models.Model):
	requester = models.ForeignKey('Profile', null=True, blank=True, related_name='requester_profile')
	friend = models.ForeignKey('Profile', related_name='requested_friend')

	class Meta:
		verbose_name = 'FriendRequest'
		verbose_name_plural = 'FriendRequest'

	def __unicode__(self):
		return self.requester.username + '->' + self.friend.username

	def __str__(self):
		return self.requester.username + '->' + self.friend.username


class Base64ImageField(serializers.ImageField):
	"""
	A Django REST framework field for handling image-uploads through raw post data.
	It uses base64 for encoding and decoding the contents of the file.

	Heavily based on
	https://github.com/tomchristie/django-rest-framework/pull/1268

	Updated for Django REST framework 3.
	"""

	def to_internal_value(self, data):
		from django.core.files.base import ContentFile
		import base64
		import six
		import uuid

		# Check if this is a base64 string
		if isinstance(data, six.string_types):
			# Check if the base64 string is in the "data:" format
			if 'data:' in data and ';base64,' in data:
				# Break out the header from the base64 content
				header, data = data.split(';base64,')

			# Try to decode the file. Return validation error if it fails.
			try:
				decoded_file = base64.b64decode(data)
			except TypeError:
				self.fail('invalid_image')

			# Generate file name:
			file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
			# Get the file name extension:
			file_extension = self.get_file_extension(file_name, decoded_file)

			complete_file_name = "%s.%s" % (file_name, file_extension,)

			data = ContentFile(decoded_file, name=complete_file_name)

		return super(Base64ImageField, self).to_internal_value(data)

	def get_file_extension(self, file_name, decoded_file):
		import imghdr

		extension = imghdr.what(file_name, decoded_file)
		extension = "jpg" if extension == "jpeg" else extension

		return extension


class ImageFile(models.Model):
	image = models.ImageField(upload_to='/images')
	added = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.image.url

	def __str__(self):
		return self.image.url


class Profile(models.Model):
	user = models.OneToOneField(User)
	friends = models.ManyToManyField('Profile', blank=True)
	challenges = models.ManyToManyField('ChallengeData', blank=True)
	points = models.IntegerField(default=0)
	avatar = models.ForeignKey(ImageFile, name='avatar', null=True, blank=True)
	friends_requests = models.ManyToManyField('FriendRequest', blank=True)

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profile'

	@property
	def username(self):
		return self.user.username

	@property
	def get_avatar(self):
		return self.avatar if self.avatar else None

	def __unicode__(self):
		return self.user.username

	def __str__(self):
		return self.user.username


class Challenge(models.Model):
	name = models.CharField(max_length=150)
	category = models.CharField(choices=CATEGORIES, max_length=2)
	value = models.IntegerField()
	description = models.TextField()
	begin = models.DateTimeField()
	end = models.DateTimeField(null=True, blank=True, )
	owner = models.ForeignKey(Profile, null=True, blank=True)

	class Meta:
		verbose_name = 'Challenge'
		verbose_name_plural = 'Challenge'

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		obj.save()


class ChallengeData(models.Model):
	challenger = models.ForeignKey(Profile, null=True, blank=True, related_name='challenger_profile')
	challenged = models.ForeignKey(Profile, related_name="challenged_profile")
	challenge = models.ForeignKey(Challenge)
	state = models.CharField(default=RECEIVED, choices=STATES, max_length=2)

	class Meta:
		verbose_name = 'ChallengeData'
		verbose_name_plural = 'ChallengeData'

	def __unicode__(self):
		return self.challenge.name

	def __str__(self):
		return self.challenge.name
