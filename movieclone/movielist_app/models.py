from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length= 200)
    website = models.URLField(max_length=100)
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.name


class WatchList(models.Model):
    title =  models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, on_delete = models.CASCADE, related_name = "watchlist")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
class Series(models.Model):
    title =  models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    num_of_episodes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, on_delete = models.CASCADE, related_name = "serieslist")
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    

class Reviews(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.rating) + '-' + self.watchlist.title