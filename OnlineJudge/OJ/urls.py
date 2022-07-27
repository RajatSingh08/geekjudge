from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.dashboardPage, name='dashboard'),
    path('account/', views.accountSettings, name="account"),

    path('problems/', views.problemPage, name='problems'),
    path('problems/<int:problem_id>/', views.descriptionPage, name='description'),
    path('problems/<int:problem_id>/verdict/',
         views.verdictPage, name='verdict'),
    path('all_submissions/', views.allSubmissionPage, name='all_submissions'),
    path('leaderboard/', views.leaderboardPage, name='leaderboard'),
]
