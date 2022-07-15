from sre_parse import expand_template
from django.db import models
from ckeditor.fields import RichTextField


'''class User(models.Model):
    Firstname = models.CharField(max_length=50, default="")
    Lastname = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=50, default="")
    password = models.CharField(max_length=25, default="")
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return (self.Firstname + " " + self.Lastname)'''


class Problem(models.Model):
    TOUGHNESS = (("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard"))
    STATUS = (("Unsolved", "Unsolved"), ("Solved", "Solved"))
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    description = RichTextField(default="")
    example = RichTextField(default="")
    difficulty = models.CharField(max_length=10, choices=TOUGHNESS)
    score = models.IntegerField(default=0)
    solved_status = models.CharField(
        max_length=10, choices=STATUS, default="Unsolved")

    def __str__(self):
        return (str(self.id) + ". " + self.name)


class TestCase(models.Model):
    id = models.BigAutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField(max_length=1000000)
    output = models.TextField(max_length=1000000)

    def __str__(self):
        return ("TestCase-" + self.id + " for problem-" + str(self.problem))


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    user_code = models.TextField(max_length=100000)
    verdict = models.CharField(max_length=100)

    def __str__(self):
        return (str(self.problem) + " " + self.time_stamp)
