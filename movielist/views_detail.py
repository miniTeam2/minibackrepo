from django.shortcuts import render, get_object_or_404
import requests
from .models import MoiveData, StaffData
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializer import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets


# 영화 제목을 받아오면 해당하는 영화의 세부정보 가져오기
class MovieDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, title_kor):
        movie = get_object_or_404(MoiveData, title_kor=title_kor)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)