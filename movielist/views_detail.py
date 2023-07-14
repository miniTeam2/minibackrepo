from django.shortcuts import render, get_object_or_404
import requests
from .models import MoiveData, StaffData, Comment
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializer import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets


class MovieDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, title_kor):
        movie = get_object_or_404(MoiveData, title_kor=title_kor)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)
    

# 코멘트를 작성한다.
# 코멘트 옆에 유저 이름 보여준다.
# 로그인 하지 않은 사람은 코멘트를 입력할 수 없게 막는다.
# 로그인 하지 않은 사람이 코멘트를 입력하려 하면 로그인 페이지로 이동할 수 있도록 메세지를 출력한다.
class CommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, title_kor):
        comments = Comment.objects.filter(movie__title_kor=title_kor)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, title_kor):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=MoiveData.objects.get(title_kor=title_kor))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)