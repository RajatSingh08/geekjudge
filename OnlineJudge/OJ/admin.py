from django.contrib import admin
from .models import Problem, TestCase, Submission

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)
