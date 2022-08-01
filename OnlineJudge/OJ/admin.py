from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, TestCase, Submission

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
admin.site.register(User)
