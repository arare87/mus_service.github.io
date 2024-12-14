from django.core.paginator import Paginator
from . models import Song, ListeningHistory, Genre
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from music.forms import LoginForm, RegisterForm
from .models import Profile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import logging
from django.db import IntegrityError
def Dologout(request):
    logout(request)
    return redirect('songs')

def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, 'Login successful!')
                return redirect('profile')  # Redirect to the profile page
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'music/login.html', {'form': form})

def registerPage(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(user=user, profile_picture=form.cleaned_data.get('profile_picture'))
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
        else:
            messages.error(request, 'Registration failed. Please check the errors.')
    return render(request, 'music/registration.html', {'form': form})

def music_player_view(request):
    song_list = Song.objects.all().order_by('title')
    context = {'page_obj': song_list}
    return render(request, 'music/player.html', context)

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
        listening_history = ListeningHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
        context = {
            'profile': profile,
            'listening_history': listening_history,
        }
        return render(request, 'music/profile.html', context)
    except Profile.DoesNotExist:
        messages.error(request, "Your profile hasn't been set up yet.")
        return redirect('register')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('login')

logger = logging.getLogger(__name__)


@login_required
def update_listening_history(request):
    if request.method == 'POST':
        try:
            song_url = request.POST.get('song_url')
            if song_url is None:
                return JsonResponse({'success': False, 'error': 'song_url missing'}, status=400)

            song_url = song_url.strip().rstrip('/')

            logger.info(f"Normalized song_url: {song_url}")
            try:
                song = Song.objects.get(audio_file=song_url)
            except Song.DoesNotExist:
                logger.exception(f"Song with URL '{song_url}' not found.")
                return JsonResponse({'success': False, 'error': 'Song not found'}, status=404)

            logger.info(f"Found song: {song}, audio_file: {song.audio_file}")

            try:
                ListeningHistory.objects.create(user=request.user, song=song)
                logger.info(f"Successfully added to listening history: User={request.user}, Song={song}")
            except IntegrityError:
                return JsonResponse({'success': True, 'message': 'Song already in history'})

            limit_history(request.user)
            return JsonResponse({'success': True})

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            return JsonResponse({'success': False, 'error': 'Server Error'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
def limit_history(user):
    excess = ListeningHistory.objects.filter(user=user).order_by('-timestamp')[20:]
    excess.delete()

def genre_view(request):
    genres = Genre.objects.all().values_list('name', flat=True)
    context = {'genres': genres}
    return render(request, 'music/compilations.html', context)

def get_songs_by_genre(request):
    if request.method == 'POST':
        genre_name = request.POST.get('genre')
        try:
            genre = Genre.objects.get(name=genre_name)
            songs = Song.objects.filter(genre=genre) # Filter songs directly by genre
            song_data = [{
                'title': song.title,
                'artist': song.artist,
                'image': song.image.url if song.image else '',
            } for song in songs]
            return JsonResponse({'songs': song_data})
        except Genre.DoesNotExist:
            return JsonResponse({'songs': []}, status=404)
    else:
        return JsonResponse({'songs': []}, status=405)