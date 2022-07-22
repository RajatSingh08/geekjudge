from django.db import models
from django.contrib.auth.models import AbstractUser
from froala_editor.fields import FroalaField


class User(AbstractUser):
    email = models.EmailField(unique=True, default="")
    total_score = models.IntegerField(default=0)
    solve_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-total_score']

    def __str__(self):
        return self.username


class Problem(models.Model):
    TOUGHNESS = (("Easy", "Easy"), ("Medium", "Medium"), ("Tough", "Tough"))
    STATUS = (("Unsolved", "Unsolved"), ("Solved", "Solved"))
    name = models.CharField(max_length=100, default="")
    description = FroalaField(default="")
    difficulty = models.CharField(max_length=10, choices=TOUGHNESS)
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=128)
    score = models.IntegerField(default=0)
    solved_status = models.CharField(
        max_length=10, choices=STATUS, default="Unsolved")

    def __str__(self):
        return self.name


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField(max_length=1000000)
    output = models.TextField(max_length=1000000)

    def __str__(self):
        return ("TestCase-" + self.id + " for problem-" + str(self.problem))


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    submission_time = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, null=True, blank=True)
    verdict = models.CharField(max_length=100)

    class Meta:
        ordering = ['-submission_time']


class Code(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    user_code = models.TextField(max_length=100000)
    language = models.CharField(max_length=10)
