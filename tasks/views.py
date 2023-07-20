from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/index.html"

    def get(self, request, *args, **kwargs):
        tasks = request.user.tasks.all()
        query = request.GET.get("query", "")
        filters = tasks.values("status").distinct()
        status = request.GET.get("status", "")

        form = self.form_class()

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(text__icontains=query))

        if status:
            tasks = tasks.filter(status=status)

        return render(
            request,
            self.template_name,
            {
                "tasks": tasks,
                "form": form,
                "query": query,
                "filters": filters,
                "status": status,
            },
        )

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


class TaskDetailView(LoginRequiredMixin, View):
    model_class = Task
    form_class = TaskForm
    template_name = "tasks/detail.html"

    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(self.model_class, pk=pk)
        if request.user != task.user:
            return redirect("/")
        return render(request, self.template_name, {"task": task})


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
