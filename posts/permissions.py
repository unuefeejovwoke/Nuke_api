from rest_framework import permissions

from .models import Post

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
    # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post
        return obj.author == request.user
    
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the post exists before checking permissions
        try:
            post = Post.objects.get(slug=view.kwargs['slug'])
        except Post.DoesNotExist:
            return False

        return request.user and (request.user.is_staff or post.author == request.user)