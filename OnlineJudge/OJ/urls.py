from django.urls import path
from . import views

# app_name = 'OJ'
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.homePage, name='dashboard'),
    path('problems/', views.problemPage, name='problems'),
    path('problems/<int:problem_id>/', views.descriptionPage, name='description'),
    path('submissions/', views.submissionPage, name='submissions'),
    path('leaderboard/', views.leaderboardPage, name='leaderboard')
]
