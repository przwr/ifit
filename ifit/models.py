# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ifit.constants import CATEGORIES, RECEIVED, STATES
from django.contrib.auth.models import User


class FriendRequest(models.Model):
	requester = models.ForeignKey('Profile', null=True, blank=True, related_name='requester')
	friend = models.ForeignKey('Profile', related_name='requested_friend')

	class Meta:
		verbose_name = 'FriendRequest'
		verbose_name_plural = 'FriendRequest'

	def __unicode__(self):
		return self.requester.username + '->' + self.friend.username

	def __str__(self):
		return self.requester.username + '->' + self.friend.username


class Profile(models.Model):
	user = models.OneToOneField(User)
	friends = models.ManyToManyField('Profile', blank=True)
	challenges = models.ManyToManyField('ChallengeData', blank=True)
	points = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='/images', name='avatar', null=True, blank=True)
	friends_requests = models.ManyToManyField('FriendRequest', blank=True)

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profile'

	@property
	def username(self):
		return self.user.username

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
	owner = models.ForeignKey(User, null=True, blank=True)

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
	user = models.ForeignKey(User)
	challenge = models.ForeignKey(Challenge)
	state = models.CharField(default=RECEIVED, choices=STATES, max_length=2)

	class Meta:
		verbose_name = 'ChallengeData'
		verbose_name_plural = 'ChallengeData'

	def __unicode__(self):
		return self.challenge.name

	def __str__(self):
		return self.challenge.name
