from django.urls import path
from . import views

app_name = 'repertoire'  # Пространство имен приложения

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('repertoire/', views.RepertoireListView.as_view(), name='repertoire_list'),
    path('repertoire/add/', views.RepertoireCreateView.as_view(), name='repertoire_add'),
    path('repertoire/search/', views.repertoire_search, name='repertoire_search'),
    
    path('music-tracks/', views.MusicTrackListView.as_view(), name='music_tracks'),
]
