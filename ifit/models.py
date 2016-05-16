# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ifit.constants import CATEGORIES, RECEIVED, STATES
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User)
	friends = models.ManyToManyField('Profile', blank=True)
	challenges = models.ManyToManyField('ChallengeData', blank=True)
	points = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='/images', name='avatar', null=True, blank=True)

	def __unicode__(self):
		return self.user.username


class Challenge(models.Model):
	name = models.CharField(max_length=150)
	category = models.CharField(choices=CATEGORIES, max_length=2)
	value = models.IntegerField()
	description = models.TextField()
	begin = models.DateTimeField()
	end = models.DateTimeField(null=True, blank=True)
	owner = models.ForeignKey(User)

	def __unicode__(self):
		return self.name


class ChallengeData(models.Model):
	user = models.ForeignKey(User)
	challenge = models.ForeignKey(Challenge)
	state = models.CharField(choices=STATES, max_length=2)

	def __unicode__(self):
		return self.challenge.name



# TODO on save set owner
