from django.shortcuts import render,HttpResponse
from musicbeats.models import Song, Watchlater, History, Channel, liked
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db.models import Case, When


def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)
    return render(request, 'musicbeats/search.html',{'songs':qs , 'query':query})

def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/musicbeats/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'musicbeats/history.html', {"history": song})


def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                message = "Your Song is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Song is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, "musicbeats/songpost.html", {'song': song, "message": message})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "musicbeats/watchlater.html", {'song': song})
    

def liked_view(request):  
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        user_likes = liked.objects.filter(user=user)

        for i in user_likes:
            if video_id == i.video_id:
                message = "Your Song is Already Liked"
                break
        else:
            like_instance = liked(user=user, video_id=video_id)
            like_instance.save()
            message = "Your Song is Successfully Liked"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, "musicbeats/songpost.html", {'song': song, "message": message})

    liked_songs = liked.objects.filter(user=request.user)
    liked_ids = [i.video_id for i in liked_songs]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(liked_ids)])
    song = Song.objects.filter(song_id__in=liked_ids).order_by(preserved)

    return render(request, "musicbeats/liked.html", {'song': song})


def songs(request):
    song =Song.objects.all()
    return render(request, 'musicbeats/songs.html',{'song':song})

def songpost(request,id):
    song=Song.objects.filter(song_id=id).first()
    return render(request, 'musicbeats/songpost.html',{'song':song})

def login(request):
    if request.method=="POST":
        username =request.POST['username']
        password =request.POST['password']
        user=authenticate(username=username,password=password)
        from django.contrib.auth import login as django_login
        # login(request,user)
        if user:
            django_login(request,user)
            return redirect('/')
        else:
            return HttpResponse("<h2>Invalid Credentials</h2>")
        
    return render(request,'musicbeats/login.html')



def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        

            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login as django_login
        # login(request, user)
        if user:
            django_login(request, user)

        channel = Channel(name=username)
        channel.save()

        return redirect('/')

    return render(request, 'musicbeats/signup.html')

def logout_user(request):
    logout(request)
    return redirect("/")

def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "musicbeats/channel.html", {"channel": chan, "song": song})


def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        # image = request.POST['image']
        image = request.FILES.get('image')  
        movie = request.POST['movie']
        # credit = request.POST['credit']
        song1 = request.FILES['file']

        song_model = Song(name=name, singer=singer, tags=tag, image=image, movie=movie, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request, "musicbeats/upload.html")