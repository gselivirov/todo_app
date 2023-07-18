from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


class TaskListView(View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/index.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        tasks = request.user.tasks.all()
        form = self.form_class()
        return render(request, self.template_name, {"tasks": tasks, "form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.user
        tasks = user.tasks.all()
        form = self.form_class(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = user
            new_task.save()
            redirect("/")
        return render(request, self.template_name, {"tasks": tasks, "form": form})
