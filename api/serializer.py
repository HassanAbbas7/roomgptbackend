from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ('id', 'username', 'email', 'password')
        # extra_kwargs = {'password': {'write_only': True}
        fields = "__all__"