from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='genre_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image = models.ImageField(upload_to='song_images/')
    audio_file = models.FileField(upload_to='song_audio/', null=True, blank=True)
    duration = models.FloatField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class ListeningHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = [['user', 'song']]

    def __str__(self):
        return f"{self.user} - {self.song} - {self.timestamp}"