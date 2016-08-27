# -*- coding: utf-8 -*-
import os

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from ifit.models import Profile, ImageFile


@receiver(post_save, sender=User)
def add_owner(sender, **kwargs):
	user = kwargs['instance']
	Profile.objects.get_or_create(user=user)


@receiver(pre_delete, sender=ImageFile)
def remove_image_file(sender, **kwargs):
	f = kwargs['instance']
	if f.image:
		if os.path.isfile(f.image.path):
			os.remove(f.image.path)


@receiver(pre_save, sender=ImageFile)
def remove_old_image_file_on_change(sender, **kwargs):
	f = kwargs['instance']
	if not f.pk:
		return False
	try:
		old_file = ImageFile.objects.get(pk=f.pk).image
	except ImageFile.DoesNotExist:
		return False

	new_file = f.image
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)
