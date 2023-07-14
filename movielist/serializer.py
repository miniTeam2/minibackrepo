from django.core import serializers
from rest_framework import serializers
from .models import MoiveData, StaffData, Comment

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
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'