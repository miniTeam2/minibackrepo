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

class ListPagination(PageNumberPagination):
    page_size = 10

class MovieDetail(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, title_kor):
        movie = get_object_or_404(MoiveData, title_kor=title_kor)
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)
    
class CommentView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, request, title_kor):
        comments = Comment.objects.filter(movie__title_kor=title_kor)
        paginator = ListPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        borders = paginator.get_paginated_response(serializer.data)
        return borders
    
    def post(self, request, title_kor):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=MoiveData.objects.get(title_kor=title_kor))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)