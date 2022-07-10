from django.contrib import admin
from .models import User, Problem, TestCase, Submission

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
