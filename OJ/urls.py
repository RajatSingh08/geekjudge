from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('reset_password/',
            auth_views.PasswordResetView.as_view(template_name="OJ/password_reset.html"),
            name="password_reset"),
    path('reset_password_sent/', 
            auth_views.PasswordResetDoneView.as_view(template_name="OJ/password_reset_sent.html"), 
            name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(template_name="OJ/password_reset_form.html"), 
            name="password_reset_confirm"),
    path('reset_password_complete/', 
            auth_views.PasswordResetCompleteView.as_view(template_name="OJ/password_reset_done.html"), 
            name="password_reset_complete"),

    path('', views.dashboardPage, name='dashboard'),
    path('account/', views.accountSettings, name="account"),

    path('problems/', views.problemPage, name='problems'),
    path('problems/<int:problem_id>/', views.descriptionPage, name='description'),
    path('problems/<int:problem_id>/verdict/',
            views.verdictPage, name='verdict'),
    path('all_submissions/', views.allSubmissionPage, name='all_submissions'),
    path('leaderboard/', views.leaderboardPage, name='leaderboard'),
]
