from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views



urlpatterns = [
   path('songs/',views.songs,name='songs'),
   path('podcast/',views.podcast,name='podcast'),
   path('premium/', views.premium, name='premium'),
   path('songs/<int:id>',views.songpost,name='songpost'),
   path('login/',views.login,name='login'),
   path('signup/',views.signup,name='signup'),
   path('logout_user', views.logout_user, name='logout_user'),
   path('watchlater/',views.watchlater,name='watchlater'),
   path('liked/',views.liked_view,name='liked'),
   path('history', views.history, name='history'),
   path('c/<str:channel>/', views.channel, name='channel'),
   path('upload', views.upload, name='upload'),
   path('search', views.search, name='search'),
   
   path('support/', views.support_page, name='support'),
   path('support/submit/', views.support_submit, name='support_submit'),
   
   
   path('profile/', views.profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]

