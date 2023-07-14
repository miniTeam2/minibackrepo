from django.urls import path, include
from . import views

app_name = 'members'

urlpatterns = [
    # path('signup/', views.signup),
    # path('login/', views.login),
    # path('logout/', views.logout),
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
]