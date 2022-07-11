from django.urls import path
from . import views

# app_name = 'OJ'
urlpatterns = [
    path('', views.HomePage, name='dashboard'),
    path('problems/', views.ProblemPage, name='problems'),
    path('description/', views.DescriptionPage, name='description'),
    path('submissions/', views.SubmissionPage, name='submissions'),
    path('leaderboard/', views.LeaderboardPage, name='leaderboard')
]
