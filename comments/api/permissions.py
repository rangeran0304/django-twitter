from rest_framework.permissions import BasePermission

class IsObjectOwner(BasePermission):

    #permission will be executed one by one
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user==obj.User