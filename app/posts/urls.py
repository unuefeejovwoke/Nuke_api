from django.urls import path
from .views import CategoryDetail, CategoryList, PostList, PostDetail

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),  # Update URL pattern for blog detail
    path("", PostList.as_view(), name="post_list"),
]
