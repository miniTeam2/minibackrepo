from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'username', 'password', 'email']