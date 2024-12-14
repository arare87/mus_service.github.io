from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('', views.music_player_view, name="songs"),
    path('login', views.loginPage, name='login'),
    path('register/', views.registerPage,name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('update_listening_history/', views.update_listening_history, name='update_listening_history'),
    path('genres/', views.genre_view, name='genres'),
    path('get_songs/', views.get_songs_by_genre, name='get_songs'),
    path('logout/', views.Dologout, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)