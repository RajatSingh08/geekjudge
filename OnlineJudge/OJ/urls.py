from django.urls import path
from . import views

# app_name = 'OJ'
urlpatterns = [
    path('', views.HomePage, name='home'),
    path('problems/', views.ProblemPage, name='problems'),
    path('description/', views.DescriptionPage, name='description'),
    path('submissions/', views.SubmissionPage, name='submissions')
]
