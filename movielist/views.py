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
    url = "https://api.hufs-likelion-movie.kro.kr/movies" # 영화 정보를 받아올 url
    res = requests.get(url) # json 형식으로 받아온다.
    movies = res.json()['movies'] # 영화 정보를 담은 리스트
    for movie in movies: # 영화 정보를 하나씩 꺼낸다.
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
        try: # 이미 db에 저장된 영화는 저장하지 않는다.
            movie_data = MoiveData(title_kor=title_kor, title_eng=title_eng, poster_url=poster_url, rating_aud=rating_aud, rating_cri=rating_cri, rating_net=rating_net, genre=genre, showtimes=showtimes, release_date=release_date, rate=rate, summary=summary)
            movie_data.save()
            for staff in movie['staff']: # 영화에 출연한 배우들의 정보를 따로 저장한다.
                name = staff['name']
                role = staff['role']
                image_url = staff['image_url']
                staff_data = StaffData(name=name, role=role, image_url=image_url, movie=movie_data)
                staff_data.save()
        except:
            pass
            
    return render(request, 'movielist/init_db.html', {'movies': movies}) # 저장된 영화 정보를 보여준다. init_db.html 안 만들어서 일단 무시

class MovieList(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        movies = MoiveData.objects.all()
        paginator = ListPagination() # 페이지네이션
        page = paginator.paginate_queryset(movies, request) # request를 통해 페이지네이션 정보를 받아온다.(ex. page=1)
        serializer = MoviePosterTitleSerializer(page, many=True) # 페이지네이션 정보를 통해 해당 페이지에 해당하는 영화 정보를 serializer에 담는다.
        borders = paginator.get_paginated_response(serializer.data) # 페이지네이션 정보를 통해 해당 페이지에 해당하는 영화 정보를 Response에 담는다.
        return borders # 페이지네이션 정보를 포함한 Response를 반환한다.
    

class SearchMovie(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [JWTAuthentication]
    def get(self, request, q):
        movies = MoiveData.objects.filter(Q(title_kor__contains = q)|Q(title_eng__contains = q))
        paginator = ListPagination()
        page = paginator.paginate_queryset(movies, request)
        serializer = MoviePosterTitleSerializer(page, many=True)
        borders = paginator.get_paginated_response(serializer.data)
        return borders
        
    
    
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
        movie = get_object_or_404(MoiveData, title_kor=title_kor) # 영화 정보를 가져온다.
        serializer = RatingSerializer(data=request.data) # request를 통해 받은 정보(평점)를 serializer에 담는다.
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie) # serializer에 담긴 정보를 db에 저장한다.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)