from django.core import serializers
from rest_framework import serializers
from .models import MoiveData, StaffData, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = '__all__'
        
class MoviePosterTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = ['poster_url', 'title_kor', 'title_eng']
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment

        fields = ['user', 'comment', 'created_at']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffData
        fields = '__all__'
    
class MovieListSerializer(serializers.ModelSerializer):
    staffs = StaffSerializer(many=True, read_only=True, source='staffdata_set')
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    class Meta:
        model = MoiveData
        fields = ['title_kor', 'title_eng', 'poster_url', 'rating_aud', 'rating_cri', 'rating_net', 'genre', 'showtimes', 'release_date', 'rate', 'summary', 'staffs', 'comments']
