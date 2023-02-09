from django.urls import path
from . import views

urlpatterns = [
    path('cepheus/', views.cepheusPage, name='cepheus'),
    path('cepheus/<str:event_name>/', views.cepheusEventsPage, name='cepheus_events'),
    path('cepheus/<str:event_name>/leaderboard', views.eventLeaderboardPage, name='event_leaderboard'),
]
