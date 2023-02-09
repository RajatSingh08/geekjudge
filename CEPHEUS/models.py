from django.db import models
from datetime import datetime
import USERS.models

###############################################################################################################################


class Event(models.Model):
    name = models.CharField(max_length=100, default="")
    start_time = models.DateTimeField(default=datetime.now, blank=True)
    end_time = models.DateTimeField(default=datetime.now, blank=True)
    registered_students = models.ManyToManyField("USERS.User")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
