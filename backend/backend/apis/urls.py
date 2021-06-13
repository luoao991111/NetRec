from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import User_Info
from .views import Song_Info
from .views import Get_lyris
from .views import Get_Record
from .views import Login
from .views import mainpage
from .views import Recommend_On_Page
from .views import Who_Listen_This

urlpatterns = [
    path('userinfo', User_Info),
    path('songinfo', Song_Info),
    path('lyric', Get_lyris),
    path('record', Get_Record),
    path('login', Login),
    path('mainpage', mainpage),
    path('wholisten', Who_Listen_This),
    path('pagerec', Recommend_On_Page)
]
