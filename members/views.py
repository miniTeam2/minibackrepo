from django.shortcuts import render
from .models import CustomUser
from .serializers import LoginSerializer, SignupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.contrib.auth.hashers import make_password


# Create your views here.

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        new_user = serializer.save(password = make_password(serializer.validated_data['password']))
        auth.login(request, new_user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializers = LoginSerializer(data = request.data)
    if serializers.is_valid():
        user = auth.authenticate(
            request=request,
            username = serializers.data['username'],
            password = serializers.data['password'],
        )
        if user is not None:
            auth.login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    return Response(status=status.HTTP_200_OK)