from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    nickname = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'nickname', 'email')