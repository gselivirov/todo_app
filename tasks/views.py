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
            return redirect("/")
        return render(request, self.template_name, {"tasks": tasks, "form": form})


class TaskDetailView(View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/detail.html"

    def get(self, request, pk, *args, **kwargs):
        task = self.model_class.objects.get(pk=pk)
        return render(request, self.template_name, {"task": task})


class TaskEditView(View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/edit.html"

    def get(self, request, pk, *args, **kwargs):
        task = self.model_class.objects.get(pk=pk)
        form = self.form_class(instance=task)
        return render(request, self.template_name, {"form": form})


    def post(self, request, pk):
        task = self.model_class.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:detail", pk)
        return render(request, self.template_name, {"form": form})

