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
from rest_framework_simplejwt.authentication import JWTAuthentication

class ListPagination(PageNumberPagination):
    page_size = 10

class MovieDetail(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request, title_kor):
        movie = get_object_or_404(MoiveData, title_kor=title_kor) # 해당 영화 정보를 가져온다.
        serializer = MovieListSerializer(movie) # 해당 영화 정보를 serializer에 담는다.
        return Response(serializer.data) # 해당 영화 정보를 Response에 담는다.
    
class CommentView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request, title_kor):
        comments = Comment.objects.filter(movie__title_kor=title_kor) # 해당 영화에 달린 댓글들을 가져온다.
        paginator = ListPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        borders = paginator.get_paginated_response(serializer.data)
        return borders
    
    def post(self, request, title_kor):
        serializer = CommentSerializer(data=request.data) # 받아온 정보(댓글)를 serializer에 담는다.
        if serializer.is_valid():
            serializer.save(user=request.user, movie=MoiveData.objects.get(title_kor=title_kor)) # serializer에 담긴 정보를 저장한다.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)