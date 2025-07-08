from django.shortcuts import render,HttpResponse , redirect
from musicbeats.models import Song, Watchlater, History, Channel, liked , Podcast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, When
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage


########   Search_views   #########
def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)
    return render(request, 'musicbeats/search.html',{'songs':qs , 'query':query})

########   History_views   #########
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

  ########   Playlist_views   #########  
def watchlater(request):
    user = request.user
    if request.method == "POST":
        video_id = request.POST['video_id']
        existing = Watchlater.objects.filter(user=user, video_id=video_id).first()

        if existing:
            existing.delete()
            message = "Removed from Playlist"
        else:
            Watchlater.objects.create(user=user, video_id=video_id)
            message = "Added to Playlist"
        song = Song.objects.filter(song_id=video_id).first()
        return render(request, "musicbeats/songpost.html", {'song': song, "message": message})
    wl = Watchlater.objects.filter(user=user)
    ids = [i.video_id for i in wl]

    preserved = Case(*[When(song_id=pk, then=pos) for pos, pk in enumerate(ids)])
    songs = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "musicbeats/watchlater.html", {'song': songs})


########   Liked_views   #########
def liked_view(request):
    user = request.user

    if request.method == "POST":
        video_id = request.POST['video_id']
        like_obj = liked.objects.filter(user=user, video_id=video_id).first()

        if like_obj:
            like_obj.delete()
            message = "Removed from Liked Songs"
        else:
            liked.objects.create(user=user, video_id=video_id)
            message = "Added to Liked Songs"
        song = Song.objects.filter(song_id=video_id).first()
        return render(request, "musicbeats/songpost.html", {'song': song, 'message': message})
    liked_songs = liked.objects.filter(user=user)
    liked_ids = [i.video_id for i in liked_songs]

    preserved = Case(*[When(song_id=pk, then=pos) for pos, pk in enumerate(liked_ids)])
    songs = Song.objects.filter(song_id__in=liked_ids).order_by(preserved)

    return render(request, "musicbeats/liked.html", {'song': songs})

########   Songs_views   #########
def songs(request):
    song =Song.objects.all()
    return render(request, 'musicbeats/songs.html',{'song':song})


########   Podcast_views   #########
def podcast(request):
    podcasts = Podcast.objects.all()
    return render(request, 'musicbeats/podcast.html',{'podcasts':podcasts})


########   Premium_views   #########
def premium(request):
    return render(request, 'premium.html')


########   SongsPost_views   #########
def songpost(request,id):
    song=Song.objects.filter(song_id=id).first()
    return render(request, 'musicbeats/songpost.html',{'song':song})


########   Login_views   ########
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
            return HttpResponse("""<div style="text-align:center; margin-top:50px;">
            <h2 style="color:red;">Invalid Credentials</h2>
            <a href="/musicbeats/login/" style="text-decoration:none;">
                <button style="margin-top:20px; padding:10px 20px; background:#dc3545; color:white; border:none; border-radius:5px;">Back to Login</button>
            </a></div>""")
        
    return render(request,'musicbeats/login.html', {'hide_nav_footer': True})


########   Signup_views   #########
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
        
        # Send thank-you email
        subject = '🎧 Welcome to Soundory!'
        # message = f"Hi {first_name},\n\nThank you for registering with Soundory.\nWe're thrilled to have you onboard!\n\nEnjoy the music! 🎶\n\n- Team Soundory"
        message = f"""
Hi {first_name},

Thank you for signing up with Soundory – your one-stop platform to experience the rhythm of life!

We’re thrilled to have you join our vibrant music community. At Soundory, you can:
🎵 Discover trending and classic songs  
📁 Create and manage your own playlists  
🔎 Explore music by your favorite artists and genres  
💚 Enjoy a personalized listening experience

Our mission is to bring joy to your ears and soul. We're constantly adding new features, so stay tuned for updates!

If you ever need help or want to give us feedback, feel free to contact us at support@soundory.com. We're here to make your journey smooth and sound-ful!

Welcome aboard, {first_name}!  
Let the music play 🎶

Warm regards,  
Team Soundory  
"""
        from_email = None  # Uses DEFAULT_FROM_EMAIL from settings.py
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('/')

    return render(request, 'musicbeats/signup.html', {'hide_nav_footer': True})

########   LogOut_views   #########
def logout_user(request):
    logout(request)
    return redirect("/")

########   Channel_views   #########
def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "musicbeats/channel.html", {"channel": chan, "song": song})

########   Upload_views   #########
def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        image = request.FILES.get('image')  
        movie = request.POST['movie']
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


########   Support_views   #########
def support_page(request):
    return render(request, 'support.html')

# def support_submit(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         message = request.POST['message']

#         full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

#         # Send email to admin/support (only if email setup is configured)
#         send_mail(
#             subject=f'Support Request from {name}',
#             message=full_message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[settings.DEFAULT_FROM_EMAIL],
#             fail_silently=False
#         )

#         messages.success(request, 'Thank you for contacting us! We’ll get back to you soon.')
#         return redirect('support')
def support_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        file = request.FILES.get('file')      # Optional file
        image = request.FILES.get('image')    # Optional image

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        email_msg = EmailMessage(
            subject=f'Support Request from {name}',
            body=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
            reply_to=[email],
        )

        # Attach files only if present
        if file:
            email_msg.attach(file.name, file.read(), file.content_type)

        if image:
            email_msg.attach(image.name, image.read(), image.content_type)

        try:
            email_msg.send()
            messages.success(request, 'Thank you for contacting us! We’ll get back to you soon.')
        except Exception as e:
            print("Error sending email:", e)
            messages.error(request, 'Sorry, there was a problem sending your message.')

        return redirect('support')

########   Profile_views   #########
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'u_form': u_form})

