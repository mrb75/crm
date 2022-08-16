from rest_framework.permissions import BasePermission


class BillViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_bill')


class BillRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_bill')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin or request.user.admin == obj.user.admin != None)


class BillAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.add_bill')


class BillChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.change_bill')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin or request.user.admin == obj.user.admin != None)


class BillRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.delete_bill')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user.admin or request.user.admin == obj.user.admin != None)


class CategoryViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_category')


class CategoryRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_category')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user or request.user.admin == obj.user != None)


class CategoryAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.add_category')


class CategoryChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.change_category')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user or request.user.admin == obj.user != None)


class CategoryRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.delete_category')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user or (request.user.admin == obj.user != None))


class ProductViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_product')


class ProductRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.view_product')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user) or (request.user == obj.category.user)


class ProductAddPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.add_product')


class ProductChangePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.change_product')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user) or (request.user == obj.category.user) or (request.user.admin == obj.user.admin != None) or (request.user.admin == obj.category.user)


class ProductRemovePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('bills.delete_product')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user) or (request.user == obj.category.user) or (request.user.admin == obj.user.admin != None) or (request.user.admin == obj.category.user)
