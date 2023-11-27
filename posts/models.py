import math
from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def reading_time_minutes(self):
        words_per_minute = 200  
        total_words = len(self.body.split())
        minutes = math.ceil(total_words / words_per_minute)
        return minutes

    def display_reading_time(self):
        minutes = self.reading_time_minutes()
        if minutes == 1:
            return "1 min read"
        else:
            return f"{minutes} mins read"
