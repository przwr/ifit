from django.contrib import admin
from ifit.models import *

admin.site.register(Challenge)
admin.site.register(ChallengeData)
admin.site.register(Profile)
admin.site.register(FriendRequest)


# Register your models here.


# TODO test adding owner
class ChallengeAdmin(admin.ModelAdmin):
	fields = ('name', 'category', 'value', 'description', 'begin', 'end')

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		obj.save()
