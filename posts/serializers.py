from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'created_at', 'updated_at', 'published', 'category', 'slug', 'image']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        post = Post.objects.create(**validated_data)

        if category_data:
            category, created = Category.objects.get_or_create(name=category_data.get('name'))
            post.category = category
            post.save()

        return post

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        instance = super().update(instance, validated_data)

        if category_data:
            instance.category, created = Category.objects.get_or_create(name=category_data.get('name'))
            instance.save()

        return instance




