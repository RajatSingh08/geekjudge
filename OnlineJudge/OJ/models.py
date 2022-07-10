from django.db import models


class User(models.Model):
    total_score = models.FloatField(default=0)


class Problem(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=100000)
    difficulty = models.CharField(max_length=10)
    solved_status = models.CharField(max_length=10)
    score = models.FloatField()

    def __str__(self):
        return self.name


class TestCase(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.CharField(max_length=1000000)
    output = models.CharField(max_length=1000000)


class Submission(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    user_code = models.CharField(max_length=100000)
    verdict = models.CharField(max_length=100)
