from rest_framework import permissions



class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permisson to allow only admins to edit
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object level permission to allow only admins or owner and to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permission are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to owner or admin 
        return obj.user == request.user or request.user.is_staff
    

class IsInquiryOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission for Inquiry
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow if user is admin or inquiry email matches user email
        return request.user.is_staff or obj.email == request.user.email