# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Challenge(models.Model):
	title = models.CharField(max_length=150)
	description = models.TextField()
	value = models.IntegerField()
