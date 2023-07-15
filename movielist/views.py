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
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTAuthentication


class ListPagination(PageNumberPagination):
    page_size = 16


# 받아온 정보를 model에 맞게 db에 저장한다.
def init_db(request):
    url = "https://api.hufs-likelion-movie.kro.kr/movies"
    res = requests.get(url)
    movies = res.json()['movies']
    for movie in movies:
        title_kor = movie['title_kor']
        title_eng = movie['title_eng']
        poster_url = movie['poster_url']
        rating_aud = movie['rating_aud']
        rating_cri = movie['rating_cri']
        rating_net = movie['rating_net']
        genre = movie['genre']
        showtimes = movie['showtimes']
        release_date = movie['release_date']
        rate = movie['rate']
        summary = movie['summary']
        try:
            movie_data = MoiveData(title_kor=title_kor, title_eng=title_eng, poster_url=poster_url, rating_aud=rating_aud, rating_cri=rating_cri, rating_net=rating_net, genre=genre, showtimes=showtimes, release_date=release_date, rate=rate, summary=summary)
            movie_data.save()
            for staff in movie['staff']:
                name = staff['name']
                role = staff['role']
                image_url = staff['image_url']
                staff_data = StaffData(name=name, role=role, image_url=image_url, movie=movie_data)
                staff_data.save()
        except:
            pass
            
    return render(request, 'movielist/init_db.html', {'movies': movies})

class MovieList(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        movies = MoiveData.objects.all()
        paginator = ListPagination()
        page = paginator.paginate_queryset(movies, request)
        serializer = MoviePosterTitleSerializer(page, many=True)
        borders = paginator.get_paginated_response(serializer.data)
        return borders
    

class SearchMovie(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request, q):
        try:
            movies = MoiveData.objects.filter(Q(title_kor__contains = q)|Q(title_eng__contains = q))
            serializer = MoviePosterTitleSerializer(movies, many=True)
            return Response(serializer.data)
        except:
            return Response()
    
    
class RatingView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    # def get(self, request, title_kor):
    #     movie = get_object_or_404(MoiveData, title_kor=title_kor)
    #     ratings = Rating.objects.filter(movie=movie)
    #     serializer = RatingSerializer(ratings, many=True)
    #     return Response(serializer.data)
    
    def post(self, request, title_kor):
        # request: 0 ~ 5 사이의 실수
        movie = get_object_or_404(MoiveData, title_kor=title_kor)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)