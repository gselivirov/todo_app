from django.urls import path
from .views import TaskListView, TaskDetailView, TaskEditView, NewTaskView, delete_task

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks"),
    path("new/", NewTaskView.as_view(), name="new"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/<int:pk>/edit/", TaskEditView.as_view(), name="edit"),
    path("task/<int:pk>/delete/", delete_task, name="delete"),
]
