from rest_framework.permissions import BasePermission


class BillViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_bill')


class BillRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_bill')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user.admin


class BillAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.add_bill')


class BillChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.change_bill')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user.admin


class BillRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.delete_bill')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user.admin
