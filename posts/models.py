import math
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.db import IntegrityError

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

def unique_slugify(instance, value):
    slug = slugify(value)
    unique_slug = slug
    num = 1
    while instance.__class__.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # Add the image field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
            while True:
                try:
                    super().save(*args, **kwargs)
                    break  # Break the loop if save is successful
                except IntegrityError:
                    # Slug collision, try generating a new unique slug
                    self.slug = unique_slugify(self, self.title)
        else:
            super().save(*args, **kwargs)

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