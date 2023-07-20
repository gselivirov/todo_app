from django import forms
from .models import Task

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl bg-gray-100"

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "text", "due_date", "status"]
        widgets = {
            "title": forms.widgets.TextInput(attrs={"class":INPUT_CLASSES}),
            "text": forms.widgets.Textarea(attrs={"class":INPUT_CLASSES}),
            "due_date": forms.widgets.DateTimeInput(attrs={"class":INPUT_CLASSES}),
            # "status": forms.widgets.(attrs={"class":INPUT_CLASSES}),
        }
