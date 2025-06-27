from django.shortcuts import render
from django.db.models import Case, When
from django.contrib.auth.models import User
from musicbeats.models import Song
from musicbeats.models import Watchlater, liked


# def index(request):
#     song =Song.objects.all()
#     return render(request,'index.html',{'song':song})
# def index(request):
#     song = Song.objects.all()[0:3]

#     if request.user.is_authenticated:
#         wl = Watchlater.objects.filter(user=request.user)
#         ids = []
#         for i in wl:
#             ids.append(i.video_id)
        
#         preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
#         watch = Song.objects.filter(song_id__in=ids).order_by(preserved) 
#         watch = reversed(watch)
    
#     else:
#         watch = Song.objects.all()[0:3]
        

#     if request.user.is_authenticated:
#         # Get liked song IDs
#         liked_songs = liked.objects.filter(user=request.user)
#         liked_ids = []
#         for i in liked_songs:
#             liked_ids.append(i.video_id)
        
#         preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
#         user_likes = Song.objects.filter(song_id__in=ids).order_by(preserved) 
#         user_likes = reversed(user_likes)
    
#     else:
#         user_likes = Song.objects.all()[0:3]

#     return render(request, 'index.html', {'song': song, 'watch': watch, 'user_likes':user_likes})

from django.shortcuts import render
from django.db.models import Case, When
# from .models import Song, Watchlater, liked

def index(request):
    song = Song.objects.all()[0:3]

    # Default values
    watch = Song.objects.all()[0:3]
    user_likes = Song.objects.all()[0:3]

    if request.user.is_authenticated:
        # Watchlater Songs
        watch_ids = list(Watchlater.objects.filter(user=request.user).values_list('video_id', flat=True))
        if watch_ids:
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(watch_ids)])
            watch_qs = Song.objects.filter(song_id__in=watch_ids).order_by(preserved)
            watch = reversed(watch_qs)

        # Liked Songs
        liked_ids = list(liked.objects.filter(user=request.user).values_list('video_id', flat=True))
        if liked_ids:
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(liked_ids)])
            likes_qs = Song.objects.filter(song_id__in=liked_ids).order_by(preserved)
            user_likes = reversed(likes_qs)

    return render(request, 'index.html', {'song': song, 'watch': watch, 'user_likes': user_likes})
