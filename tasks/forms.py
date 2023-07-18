from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "text", "due_date",]
        widgets = {
            "title": forms.widgets.TextInput(),
            "due_date": forms.widgets.DateTimeInput(),
        }

    