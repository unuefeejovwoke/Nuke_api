from rest_framework import generics, status,  permissions
from rest_framework.response import Response
from .permissions import IsAdminUser, IsAuthorOrAdminOrReadOnly, IsAuthorOrReadOnly
from .models import Category, Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import CategorySerializer, PostSerializer

from rest_framework import permissions

class ReadOnlyOrAdminCategoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to the CategoryList for all users
        if request.method in permissions.SAFE_METHODS and view.__class__.__name__ == "CategoryList":
            return True

        # Allow only admin users to create categories
        return request.user and request.user.is_staff

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [ReadOnlyOrAdminCategoryPermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(published=True)

    def perform_create(self, serializer):
        category_data = self.request.data.get('category')
        serializer.is_valid(raise_exception=True)

        if category_data:
            category, created = Category.objects.get_or_create(name=category_data['name'])
            serializer.validated_data['category'] = category

        serializer.save(author=self.request.user, published=True)


    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [IsAdminUser()]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Post.DoesNotExist:
            return Response({"detail": "No post available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)