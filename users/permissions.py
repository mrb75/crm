from rest_framework.permissions import BasePermission


class SubUsersViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_user')


class SubUsersAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.add_user')


class SubUsersChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_user')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin or (request.user.admin == obj.admin)


class SubUsersDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_user')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin


class UserImageViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_userimage')


class UserImageAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.add_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin or (request.user.admin == obj.admin)


class UserImageChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin or (request.user.admin == obj.admin)


class UserImageDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin
