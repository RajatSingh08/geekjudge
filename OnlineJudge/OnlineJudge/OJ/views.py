'''
List of Views:
- REGISTER PAGE: To register a new user.
- LOGIN PAGE: To login a registered user.
- LOGOUT PAGE: To logout a registered user.
- DASHBOARD PAGE: Has a dashboard with stats.
- PROBLEM PAGE: Has the list of problems with sorting & paginations.
- DEESCRIPTION PAGE: Shows problem description of left side and has a text editor on roght side with code submit buttton.
- SUBMIT PAGE: Accepts a solution and redirects to verdict.html
- SUBMISSIONS PAGE: To view all the submissions made by current logged-in user.
- LEADERBOARD: Diplay the leaderboard.
'''
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import User, Problem, TestCase, Submission
from .forms import CreateUserForm


# To register a new user
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


# To login a registered user
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


# To logout a registered user
def logoutPage(request):
    logout(request)
    return redirect('login')


# To show stats in dashboards
@login_required(login_url='login')
def dashboardPage(request):
    return render(request, 'OJ/dashboard.html')


# Has the list of problems with sorting & paginations
@login_required(login_url='login')
def problemPage(request):
    problems = Problem.objects.all()
    return render(request, 'OJ/problem.html', {'problems': problems})


# Shows problem description of left side and has a text editor on roght side with code submit buttton.
@login_required(login_url='login')
def descriptionPage(request, problem_id):
    user_id = request.user.id
    problem = get_object_or_404(Problem, id=problem_id)
    user = User.objects.get(id=user_id)
    context = {'problem': problem, 'user': user, 'user_id': user_id}
    return render(request, 'OJ/description.html', context)


# Accepts a solution and redirects to verdict.html
@login_required(login_url='login')
def verdictPage(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    context = {'problem': problem}
    return render(request, 'OJ/verdict.html')


@login_required(login_url='login')
def submissionPage(request):
    return render(request, 'OJ/submission.html')


# Diplay the leaderboard
@login_required(login_url='login')
def leaderboardPage(request):
    return render(request, 'OJ/leaderboard.html')
