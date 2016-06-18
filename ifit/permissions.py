from rest_framework import permissions


class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Permissions are only allowed to the owner.
		return obj.owner == request.user


class IsUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Permissions are only allowed to the owner.
		return obj.user == request.user


class IsSuperUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Permissions are only allowed to the owner.
		return request.user.is_superuser


class IsThisUserOrSuperUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Permissions are only allowed to the owner.
		return request.user.is_superuser or obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner.
		return obj.owner == request.user


class IsUserOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# Write permissions are only allowed to the owner.
		return obj.user == request.user
