from distutils.command.build_scripts import first_line_re
from django.db import models
from django.contrib.auth.models import AbstractUser
from froala_editor.fields import FroalaField


###############################################################################################################################


class User(AbstractUser):
    email = models.EmailField(unique=True, default="")
    total_score = models.IntegerField(default=0)
    easy_solve_count = models.IntegerField(default=0)
    medium_solve_count = models.IntegerField(default=0)
    tough_solve_count = models.IntegerField(default=0)
    total_solve_count = models.IntegerField(default=0)
    full_name = models.CharField(max_length=50, default="")
    profile_pic = models.ImageField(
        default="defaultpic.png", blank=True, null=True, upload_to='')

    class Meta:
        ordering = ['-total_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_name = self.first_name+" "+self.last_name

    def __str__(self):
        return self.username


###############################################################################################################################

class Problem(models.Model):
    TOUGHNESS = (("Easy", "Easy"), ("Medium", "Medium"), ("Tough", "Tough"))
    STATUS = (("Unsolved", "Unsolved"), ("Solved", "Solved"))
    name = models.CharField(max_length=100, default="")
    description = FroalaField(default="")
    difficulty = models.CharField(max_length=10, choices=TOUGHNESS)
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=128)

    def __str__(self):
        return self.name


###############################################################################################################################


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return ("TC for problem: " + str(self.problem))


###############################################################################################################################


class Submission(models.Model):
    LANGUAGES = (("C++", "C++"), ("C", "C"))
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    problem = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
    user_code = models.TextField(max_length=100000, default="")
    submission_time = models.DateTimeField(auto_now_add=True, null=True)
    language = models.CharField(
        max_length=10, choices=LANGUAGES, default="C++")
    verdict = models.CharField(max_length=100, default="Wrong Answer")

    class Meta:
        ordering = ['-submission_time']

    def __str__(self):
        return str(self.submission_time) + " : @" + str(self.user) + " : " + self.problem.name + " : " + self.verdict
