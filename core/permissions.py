from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allow only admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsStaff(permissions.BasePermission):
    """Allow only staff users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'staff'


class IsStudent(permissions.BasePermission):
    """Allow only students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsAdminOrStaff(permissions.BasePermission):
    """Allow admins and staff."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'staff']
        )
        
#Object-Level Permissions
class IsOwnerOrAdmin(permissions.BasePermission):
    """Only the owner or admin can modify."""
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (obj == request.user or request.user.role == 'admin')
        )