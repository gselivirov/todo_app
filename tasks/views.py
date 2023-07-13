from django.shortcuts import render
from django.views import View

from .models import Task


class TaskListView(View):
    model_class = Task

    def get(self, request, *args, **kwargs):
        task = self.model_class.objects.get(pk=1)
        return render(request, "tasks/task_list.html", {"title": task.title})
