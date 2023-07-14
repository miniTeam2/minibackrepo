from rest_framework import serializers
from .models import CustomUser
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

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

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'nickname')


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=100)
    
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', '')
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.nickname = self.cleaned_data.get('nickname')
        user.save()
        adapter.save_user(request, user, self)
        return user
    

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname']