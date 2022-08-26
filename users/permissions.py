from rest_framework.permissions import BasePermission


class SubUsersViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_user')


class SubUserRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_user')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


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


class UserImageRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class UserImageAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.add_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin or (request.user.admin == obj.admin)


class UserImageChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user.admin or (request.user.admin == obj.user.admin)


class UserImageDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_userimage')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user.admin


class TicketViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_ticket')


class TicketRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_ticket')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class TicketAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.add_ticket')


class TicketChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_ticket')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class TicketRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_ticket')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="admin_user").exists()


class TurnViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_turn')


class TurnRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.view_turn')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin) or (request.user.admin == obj.user.admin)


class TurnAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.add_turn')


class TurnChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.change_turn')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin) or (request.user.admin == obj.user.admin)


class TurnRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.delete_turn')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin) or (request.user.admin == obj.user.admin)
