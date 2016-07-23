# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from ifit.models import Challenge, Profile



@receiver(post_save, sender=User)
def add_owner(sender, **kwargs):
	user = kwargs['instance']
	Profile.objects.get_or_create(user=user)
