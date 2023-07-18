from django.urls import path
from .views import TaskListView, TaskDetailView, TaskEditView

app_name = "tasks"

urlpatterns = [
    path("", TaskListView.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("task/<int:pk>/edit/", TaskEditView.as_view(), name="edit"),
]
