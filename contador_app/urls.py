from django.urls import path
from . import views

app_name = 'counter_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('get_count/', views.get_count, name='get_count'),
]