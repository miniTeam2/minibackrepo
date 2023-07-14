from django.urls import path, include
from . import views
from . import views_detail
from rest_framework import routers

app_name = 'movielist'

urlpatterns = [
    path('', views.init_db),
    path('movies/', views.MovieList.as_view()),
    path('detail/<str:title_kor>/', views_detail.MovieDetail.as_view()),
    # path('movies/', views.MovieList.as_view({'get': 'list'})),
    # path('init_db/', views.init_db)
]