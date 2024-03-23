from rest_framework.permissions import BasePermission

class IsFarmer(BasePermission):
    """
    Custom permission to only allow farmers to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a farmer
        return request.user and request.user.is_authenticated and request.user.is_farmer
