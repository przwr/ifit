from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ifit.models import *

# admin.site.register(Challenge)
admin.site.register(ChallengeData)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.unregister(User)


# TODO test adding owner
class ChallengeAdmin(admin.ModelAdmin):
	fields = ('name', 'category', 'value', 'description', 'begin', 'end')

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		obj.save()


# class ChallengeDataAdmin(admin.ModelAdmin):
# 	fields = ('challenger', 'challenged', 'challenge', 'state')
#
# 	def save_model(self, request, obj, form, change):
# 		obj.challenger = request.user.profile
# 		obj.save()


class UserProfileInline(admin.StackedInline):
	model = Profile


class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline, ]


admin.site.register(Challenge, ChallengeAdmin)
# admin.site.register(ChallengeData, ChallengeDataAdmin)
admin.site.register(User, UserProfileAdmin)
