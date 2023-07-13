from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    # status = models.CharField()
