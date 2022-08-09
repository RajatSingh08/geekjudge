'''
List of Views:
- REGISTER PAGE: To register a new user.
- LOGIN PAGE: To login a registered user.
- LOGOUT PAGE: To logout a registered user.
- ACOOUNT SETTINGS PAGE : To update profile pic and full name.
- DASHBOARD PAGE: Has a dashboard with stats.
- PROBLEM PAGE: Has the list of problems with sorting & paginations.
- DEESCRIPTION PAGE: Shows problem description of left side and has a text editor on roght side with code submit buttton.
- VERDICT PAGE: Shows the verdict to the submission.
- SUBMISSIONS PAGE: To view all the submissions made by current logged-in user.
- LEADERBOARD: Diplay the leaderboard.
'''
from ast import Sub

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str

from .tokens import account_activation_token
from .models import User, Problem, TestCase, Submission
from .forms import CreateUserForm, UpdateProfileForm
from datetime import datetime

import os
import sys
import subprocess
import os.path
import docker



###############################################################################################################################
# To register a new user
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            if User.objects.filter(email=user_email).exists():
                messages.error(request,'Email already exist!')
                context = {'form': form}
                return render(request, 'OJ/register.html', context)

            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Account created successfully! Please verify your email by clicking on the link sent to your email address')

            username = form.cleaned_data.get('username')
            current_site = get_current_site(request)
            email_subject = "Confirm your email!"
            email_message = render_to_string('OJ/email_confirmation.html',{
                'name':username,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                to=[to_email],
            )
            email.fail_silently = True
            email.send()

            return redirect('login')

    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'OJ/register.html', context)



###############################################################################################################################
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



###############################################################################################################################
# To activate user account via email verification
def activate(request,uidb64,token):
  try:
    uid=force_str(urlsafe_base64_decode(uidb64))
    user=User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user=None
  
  if user is not None and account_activation_token.check_token(user,token):
    user.is_active=True
    user.save()
    login(request,user)
    return redirect('dashboard')
  else:
    messages.error(request,'Activation failed, Please try again!')
    return render(request,'OJ/register.html')



###############################################################################################################################
# To logout a registered user
def logoutPage(request):
    logout(request)
    return redirect('login')



###############################################################################################################################
# to update prfile pic and full name
@login_required(login_url='login')
def accountSettings(request):
    form = UpdateProfileForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'OJ/account_settings.html', context)



###############################################################################################################################
# To show stats in dashboards
@login_required(login_url='login')
def dashboardPage(request):
    total_ques_count = len(Problem.objects.all())
    easy_ques_count = len(Problem.objects.filter(difficulty="Easy"))
    medium_ques_count = len(Problem.objects.filter(difficulty="Medium"))
    tough_ques_count = len(Problem.objects.filter(difficulty="Tough"))

    user = request.user
    easy_solve_count = user.easy_solve_count
    medium_solve_count = user.medium_solve_count
    tough_solve_count = user.tough_solve_count
    total_solve_count = user.total_solve_count

    easy_progress = (easy_solve_count/easy_ques_count)*100
    medium_progress = (medium_solve_count/medium_ques_count)*100
    tough_progress = (tough_solve_count/tough_ques_count)*100
    total_progress = (total_solve_count/total_ques_count)*100

    context = {"easy_progress":easy_progress,"medium_progress":medium_progress,
                "tough_progress":tough_progress,"total_progress":total_progress,
                "easy_solve_count":easy_solve_count, "medium_solve_count":medium_solve_count, 
                "tough_solve_count":tough_solve_count,"total_solve_count":total_solve_count,
                "easy_ques_count":easy_ques_count, "medium_ques_count":medium_ques_count, 
                "tough_ques_count":tough_ques_count,"total_ques_count":total_ques_count}
    return render(request, 'OJ/dashboard.html', context)



###############################################################################################################################
# Has the list of problems with sorting & paginations
@login_required(login_url='login')
def problemPage(request):
    problems = Problem.objects.all()
    submissions = Submission.objects.filter(user=request.user, verdict="Accepted")
    accepted_problems = []
    for submission in submissions:
        accepted_problems.append(submission.problem_id)
    context = {'problems': problems, 'accepted_problems': accepted_problems}
    return render(request, 'OJ/problem.html', context)



###############################################################################################################################
# Shows problem description of left side and has a text editor on roght side with code submit buttton.
@login_required(login_url='login')
def descriptionPage(request, problem_id):
    user_id = request.user.id
    problem = get_object_or_404(Problem, id=problem_id)
    user = User.objects.get(id=user_id)
    context = {'problem': problem, 'user': user, 'user_id': user_id}
    return render(request, 'OJ/description.html', context)



###############################################################################################################################
# Shows the verdict to the submission
@login_required(login_url='login')
def verdictPage(request, problem_id):
    if request.method == 'POST':
        # setting docker-client
        docker_client = docker.from_env()
        Running = "running"

        problem = Problem.objects.get(id=problem_id)
        # score of a problem
        if problem.difficulty=="Easy":
            score = 10
        elif problem.difficulty=="Medium":
            score = 30
        else:
            score = 50
        testcase = TestCase.objects.get(problem_id=problem_id)
        #replacing \r\n by \n in original output to compare it with the usercode output
        testcase.output = testcase.output.replace('\r\n','\n').strip() 
        #converting input testcase to bytes to give them as input in subprocess
        tc_input = bytes(testcase.input, 'utf-8')
        #setting verdict to wrong by default
        verdict = "Wrong Answer" 
        lang = ""
        res = ""

        # if code submitted by textarea
        if request.POST['user_code']:
            user_code = request.POST['user_code']
            user_code = user_code.replace('\r\n','\n').strip()
            language = request.POST['language']
            lang = str(language)

            # if user code is in C++
            if language == "C++":
                # copy code to .cpp file
                filepath = settings.FILES_DIR + "/fcpp.cpp"
                cpp_code = open(filepath,"w")
                cpp_code.write(user_code)
                cpp_code.close()

                # checking if the docker container is running or not
                try:
                    container = docker_client.containers.get('oj-cpp')
                    container_state = container.attrs['State']
                    container_is_running = (container_state['Status'] == Running)
                    if not container_is_running:
                        subprocess.run("docker start oj-cpp",shell=True)
                except docker.errors.NotFound:
                    subprocess.run("docker run -dt --name oj-cpp gcc",shell=True)

                # copy/paste the .cpp file in docker container 
                subprocess.run(f"docker cp {filepath} oj-cpp:/fcpp.cpp",shell=True)
                # compiling the code
                res = subprocess.run("docker exec oj-cpp g++ -o output fcpp.cpp",capture_output=True,shell=True)
                # checking if the code have errors
                if res.stderr.decode('utf-8') != "":
                    verdict = "Compilation Error"
                # running the code on given input and taking the output in a variable in bytes
                res = subprocess.run("docker exec -i oj-cpp ./output",input=tc_input,capture_output=True,shell=True)
                # removing the .cpp and .output file form the container
                subprocess.run("docker exec oj-cpp rm fcpp.cpp",shell=True)
                subprocess.run("docker exec oj-cpp rm output",shell=True)

            elif language == "C":
                filepath = settings.FILES_DIR + "/fc.c"
                c_code = open(filepath,"w")
                c_code.write(user_code)
                c_code.close()
                 
                try:
                    container = docker_client.containers.get('oj-c')
                    container_state = container.attrs['State']
                    container_is_running = (container_state['Status'] == Running)
                    if not container_is_running:
                        subprocess.run("docker start oj-c",shell=True)
                except docker.errors.NotFound:
                    subprocess.run("docker run -dt --name oj-c gcc",shell=True)

                subprocess.run(f"docker cp {filepath} oj-c:/fc.c",shell=True)
                res = subprocess.run("docker exec oj-c g++ -o output fc.c",capture_output=True,shell=True)
                if res.stderr.decode('utf-8') != "":
                    verdict = "Compilation Error"
                res = subprocess.run("docker exec -i oj-c ./output",input=tc_input,capture_output=True,shell=True)
                subprocess.run("docker exec oj-c rm fc.c",shell=True)
                subprocess.run("docker exec oj-c rm output",shell=True)


        # else if code submitted by file
        elif request.FILES['codefile']:
            user_code_file = request.FILES['codefile']
            fs = FileSystemStorage()
            fs.save(user_code_file.name, user_code_file)
            file_type = str(user_code_file.name)
            cpp_lan = file_type.find(".cpp")
            c_lan = file_type.find(".c")
            filepath = settings.MEDIA_ROOT + "/" + user_code_file.name
            user_code = open(filepath, 'r').read()


            # if user code file is in C++
            if cpp_lan != -1:
                lang = "C++"

                try:
                    container = docker_client.containers.get('oj-cpp')
                    container_state = container.attrs['State']
                    container_is_running = (container_state['Status'] == Running)
                    if not container_is_running:
                        subprocess.run("docker start oj-cpp",shell=True)
                except docker.errors.NotFound:
                    subprocess.run("docker run -dt --name oj-cpp gcc",shell=True)

                subprocess.run(f"docker cp {filepath} oj-cpp:/fcpp.cpp",shell=True)
                res = subprocess.run("docker exec oj-cpp g++ -o output fcpp.cpp",capture_output=True,shell=True)
                if res.stderr.decode('utf-8') != "":
                    print(res.stderr)
                    verdict = "Compilation Error" 
                res = subprocess.run("docker exec -i oj-cpp ./output",input=tc_input,capture_output=True,shell=True)
                subprocess.run("docker exec oj-cpp rm fcpp.cpp",shell=True)
                subprocess.run("docker exec oj-cpp rm output",shell=True)
            
            # if user code file is in C
            elif c_lan != -1:
                lang = "C"

                try:
                    container = docker_client.containers.get('oj-c')
                    container_state = container.attrs['State']
                    container_is_running = (container_state['Status'] == Running)
                    if not container_is_running:
                        subprocess.run("docker start oj-c",shell=True)
                except docker.errors.NotFound:
                    subprocess.run("docker run -dt --name oj-c gcc",shell=True)

                subprocess.run(f"docker cp {filepath} oj-c:/fc.c",shell=True)
                res=subprocess.run("docker exec oj-c g++ -o output fc.c",capture_output=True,shell=True)
                if res.stderr.decode('utf-8') != "":
                    verdict = "Compilation Error"
                res = subprocess.run("docker exec -i oj-c ./output",input=tc_input,capture_output=True,shell=True)
                subprocess.run("docker exec oj-c rm fc.c",shell=True)
                subprocess.run("docker exec oj-c rm output",shell=True)

            # if user code file is invalid
            else:
                os.remove(filepath)
                user_id = request.user.id
                problem = get_object_or_404(Problem, id=problem_id)
                user = User.objects.get(id=user_id)
                context = {'problem': problem, 'user': user, 'user_id': user_id, 'invalid_file':'Invalid file'}
                return render(request, 'OJ/description.html', context)


        user_stdout = res.stdout.decode('utf-8')
        user_stderr = res.stderr.decode('utf-8')
        res=res.stdout.decode('utf-8') # converting the res variable from bytes to string
        if str(res)==str(testcase.output):
            verdict = "Accepted" 
        testcase.output += '\n' # added extra line to compare user output having extra ling at the end of their output
        if str(res)==str(testcase.output):
            verdict = "Accepted"


        # creating Solution class objects and showing it on leaderboard
        user = User.objects.get(username=request.user)
        previous_verdict = Submission.objects.filter(user=user.id, problem=problem, verdict="Accepted")
        if len(previous_verdict)==0 and verdict=="Accepted":
            user.total_score += score
            user.total_solve_count += 1
            if problem.difficulty == "Easy":
                user.easy_solve_count += 1
            elif problem.difficulty == "Medium":
                user.medium_solve_count += 1
            else:
                user.tough_solve_count += 1
            user.save()

        submission = Submission(user=request.user, problem=problem, submission_time=datetime.now(), language=lang, verdict=verdict, user_code=user_code, user_stdout=user_stdout, user_stderr=user_stderr)
        submission.save()
        os.remove(filepath)
        context={'verdict':verdict}

    return render(request,'OJ/verdict.html',context)



###############################################################################################################################
# To view all the submissions made by current logged-in user
@login_required(login_url='login')
def allSubmissionPage(request):
    submissions = Submission.objects.filter(user=request.user.id)
    return render(request, 'OJ/submission.html', {'submissions': submissions})



###############################################################################################################################
# Diplay the leaderboard
@login_required(login_url='login')
def leaderboardPage(request):
    coders = User.objects.all()
    return render(request, 'OJ/leaderboard.html', {'coders': coders})
