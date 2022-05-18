from platformdirs import user_cache_dir
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in list(SAFE_METHODS):
            return True
        return bool(request.user and request.user.is_staff)

class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return request.user.approve == True and request.user.role == 'director'


class DirectorUpdatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in list(SAFE_METHODS):
            return True
        
        return bool(request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in list(SAFE_METHODS):
            return True
        
        if 'approve' in request.data.keys():
            return request.user.is_staff
        return obj == request.user

class IsDeputy(BasePermission):
    

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "deputy"



class IsWorker(BasePermission):
    

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "worker"

