from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    LOW_PRIORITY = "low_priority"
    HIGH_PRIORITY = "high_priority"
    STATUS_CHOICES = [
        (LOW_PRIORITY, "Low priority"),
        (HIGH_PRIORITY, "High priority"),
    ]


    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=LOW_PRIORITY)

    def __str__(self):
        return str(self.title)
