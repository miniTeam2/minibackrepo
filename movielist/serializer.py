from django.core import serializers
from rest_framework import serializers
from .models import MoiveData, StaffData, Comment, Rating

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = '__all__'
        
class MoviePosterTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoiveData
        fields = ['poster_url', 'title_kor', 'title_eng']
        
class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    movie = serializers.ReadOnlyField(source='movie.title_kor')
    
    def validate_rating(self, value):
        if 0 <= value <= 5:
            return value
        else:
            raise serializers.ValidationError("Rating must be between 0 and 5")
    
    class Meta:
        model = Rating                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        fields = ['user', 'movie', 'rating']
        
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
    avg_rating = serializers.SerializerMethodField()
    
    def get_avg_rating(self, obj):
        ratings = Rating.objects.filter(movie=obj)
        if 0 < len(ratings):
            total_rating = 0
            for rating in ratings:
                total_rating += rating.rating
            avg_rating = total_rating / len(ratings)
            return avg_rating
        else:
            return 0
    
    class Meta:
        model = MoiveData
        fields = ['title_kor', 'title_eng', 'poster_url', 'rating_aud', 'rating_cri', 'rating_net', 'genre', 'showtimes', 'release_date', 'rate', 'summary', 'avg_rating', 'staffs', 'comments']
