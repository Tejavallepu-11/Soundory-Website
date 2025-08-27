from django.shortcuts import render
from django.db.models import Case, When
from django.contrib.auth.models import User
from musicbeats.models import Song
from musicbeats.models import Watchlater, liked, History
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Case, When


@login_required(login_url='/musicbeats/login/')
def index(request):
    song = Song.objects.all()[0:5]

    # Default values
    # watch = Song.objects.all()
    # user_likes = Song.objects.all()
    watch = Song.objects.none()
    user_likes = Song.objects.none()

    # Only if user is authenticated (ensured by @login_required)
    watch_ids = list(Watchlater.objects.filter(user=request.user).values_list('video_id', flat=True))
    if watch_ids:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(watch_ids)])
        watch_qs = Song.objects.filter(song_id__in=watch_ids).order_by(preserved)
        watch = reversed(watch_qs)

    liked_ids = list(liked.objects.filter(user=request.user).values_list('video_id', flat=True))
    if liked_ids:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(liked_ids)])
        likes_qs = Song.objects.filter(song_id__in=liked_ids).order_by(preserved)
        user_likes = reversed(likes_qs)
    
    
    return render(request, 'index.html', {'song': song, 'watch': watch, 'user_likes': user_likes})
