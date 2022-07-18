'''
List of Views:
- AUTHENTICATION: Sign Up/Sign In (will add at the end).
- HOME PAGE: Has a dashboard with stats.
- PROBLEM DETAIL: Once a problem is selected, user will be redirected to this page 
                  which has problem details, programming language selection drop-down menu, code submit button.
- VERDICT PAGE: Once the code is submitted, user will be redirected to this page which will show the verdict 
                and first point of difference is output is wrong.
- SUBMISSIONS: To view all the submissions made by that user.
- LEADERBOARD: Diplay the leaderboard.
'''
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.paginator import Paginator

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Problem, TestCase, Submission
from .forms import CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'OJ/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username/Password is incorrect')

        context = {}
        return render(request, 'OJ/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def homePage(request):
    return render(request, 'OJ/dashboard.html')


@login_required(login_url='login')
def problemPage(request):
    problems = Problem.objects.all()
    return render(request, 'OJ/problem.html', {'problems': problems})


@login_required(login_url='login')
def descriptionPage(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    return render(request, 'OJ/description.html', {'problem': problem})


@login_required(login_url='login')
def submissionPage(request):
    return render(request, 'OJ/submission.html')


@login_required(login_url='login')
def leaderboardPage(request):
    return render(request, 'OJ/leaderboard.html')
