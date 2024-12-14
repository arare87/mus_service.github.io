from django.contrib import admin
from .models import Song, Genre, ListeningHistory

admin.site.register(Song)
admin.site.register(ListeningHistory)
admin.site.register(Genre)