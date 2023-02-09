from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboardPage, name='dashboard'),
    path('problems/', views.problemPage, name='problems'),
    path('problems/<str:problem_name>/', views.descriptionPage, name='description'),
    path('problems/<str:problem_name>/verdict/', views.verdictPage, name='verdict'),
    path('leaderboard/', views.leaderboardPage, name='leaderboard'),
]
