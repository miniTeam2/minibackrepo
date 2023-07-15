from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator

class MoiveData(models.Model):
    title_kor = models.CharField(max_length=100, unique=True)
    title_eng = models.CharField(max_length=100, unique=True)
    poster_url = models.TextField()
    rating_aud = models.CharField(max_length=100)
    rating_cri = models.CharField(max_length=100)
    rating_net = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    showtimes = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    summary = models.TextField()
    
    def __str__(self):
        return self.title
    
class StaffData(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image_url = models.TextField()
    movie = models.ForeignKey(MoiveData, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey('members.CustomUser', on_delete=models.CASCADE)
    movie = models.ForeignKey(MoiveData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    
    def __str__(self):
        return self.comment

class Rating(models.Model):
    user = models.ForeignKey('members.CustomUser', on_delete=models.CASCADE)
    movie = models.ForeignKey(MoiveData, on_delete=models.CASCADE)
    # 0~5 사이의 값만 받도록 설정
    # rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.rating