from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from USERS.models import User, Submission
from OJ.models import Problem, TestCase
from CEPHEUS.models import Event

import pytz
import os
import sys
import os.path
from datetime import datetime


###############################################################################################################################

# To show the list of events
@login_required(login_url='login')
def cepheusPage(request):
    events = Event.objects.filter(registered_students=request.user)
    context = {'events': events}
    return render(request, 'CEPHEUS/cepheus.html', context)


###############################################################################################################################

# to show the list of assignmnets of particular course
@login_required(login_url='login')
def cepheusEventsPage(request, event_name):
    event_name = event_name.replace('_', ' ')
    event = Event.objects.get(name=event_name)
    naive_datetime = datetime.now()
    aware_datetime = pytz.timezone("Asia/Kolkata").localize(naive_datetime)

    if aware_datetime < event.start_time:
        return render(request, 'CEPHEUS/event_not_started.html')
    if aware_datetime > event.end_time:
        return render(request, 'CEPHEUS/event_ended.html')

    registered_students = User.objects.filter(event=event)
    if request.user not in registered_students:
        return render(request, 'CEPHEUS/not_registered.html')

    problems = Problem.objects.filter(event=event)
    submissions = Submission.objects.filter(user=request.user, verdict="Accepted")
    accepted_problems = []
    for submission in submissions:
        accepted_problems.append(submission.problem_id)
    context = {'problems': problems, 'accepted_problems': accepted_problems, 'event': event}
    return render(request, 'CEPHEUS/cepheus_events.html', context)


###############################################################################################################################

# Diplay the leaderboard of a particular assignment
@login_required(login_url='login')
def eventLeaderboardPage(request, event_name):
    event_name = event_name.replace('_', ' ')
    event = Event.objects.get(name=event_name)
    registered_students = User.objects.filter(event=event)
    if request.user not in registered_students:
        return render(request, 'CEPHEUS/not_registered.html')

    problems = Problem.objects.filter(event=event)
    event_scores = {}
    for student in registered_students:
        event_scores[student] = 0
        submissions = Submission.objects.filter(user=student, verdict="Accepted")
        already_evaluated = []
        languages_used = []
        for submission in submissions:
            if submission.problem in problems and submission.problem not in already_evaluated:
                if submission.submission_time > event.end_time:
                    continue
                if event.name == "Polyglot" and submission.language in languages_used:
                    continue
                if submission.problem.difficulty == "Easy":
                    event_scores[student] += 10
                elif submission.problem.difficulty == "Medium":
                    event_scores[student] += 30
                else:
                    event_scores[student] += 50
                already_evaluated.append(submission.problem)
                languages_used.append(submission.language)
    context = {'event_scores': event_scores, 'event': event}
    # print(event_scores)
    return render(request, 'CEPHEUS/event_leaderboard.html', context)
