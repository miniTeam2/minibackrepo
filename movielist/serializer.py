from django.core import serializers
from rest_framework import serializers
from .models import MoiveData, StaffData

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = '__all__'
        
class MoviePosterTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = ['poster_url', 'title_kor']