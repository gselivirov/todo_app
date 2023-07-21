from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/index.html"

    def get(self, request, *args, **kwargs):
        tasks = request.user.tasks.all()

        query = request.GET.get("query", "")
        filters = Task.STATUS_CHOICES
        status = request.GET.get("status", "")

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(text__icontains=query))

        if status:
            tasks = tasks.filter(status=status)

        overdue_tasks = tasks.filter(due_date__lte=timezone.now() - timedelta(days=1))
        today_tasks = tasks.filter(due_date__date=timezone.now())
        tomorrow_tasks = tasks.filter(due_date__date=timezone.now() + timedelta(days=1))
        week_tasks = tasks.filter(
            Q(due_date__gt=timezone.now() + timedelta(days=1))
            & Q(due_date__lte=timezone.now() + timedelta(days=7))
        )
        other_tasks = tasks.filter(due_date__gt=timezone.now() + timedelta(days=7))

        return render(
            request,
            self.template_name,
            {
                "tasks": other_tasks,
                "query": query,
                "filters": filters,
                "status": status,
                "overdue_tasks": overdue_tasks,
                "tomorrow_tasks": tomorrow_tasks,
                "week_tasks": week_tasks,
                "today_tasks": today_tasks,
            },
        )


class TaskDetailView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/detail.html"

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(self.model_class, pk=pk)
        if request.user != task.user:
            return redirect("/")
        return render(request, self.template_name, {"task": task})


class NewTaskView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/new.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("/")
        return render(request, self.template_name, {"form": form})


class TaskEditView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/edit.html"

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(self.model_class, pk=pk)
        if request.user != task.user:
            return redirect("/")
        form = self.form_class(instance=task)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        task = get_object_or_404(self.model_class, pk=pk)
        if request.user != task.user:
            return redirect("/")
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:detail", pk)
        return render(request, self.template_name, {"form": form})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.user:
        return redirect("/")
    task.delete()
    return redirect("/")
