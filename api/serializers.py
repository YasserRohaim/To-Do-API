from .models import Categories, Tasks
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields="__all__"
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields="__all__"
