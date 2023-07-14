from django.db import models

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