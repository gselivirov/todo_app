from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl"

# username = forms.CharField(widget=forms.TextInput(attrs={
#     "placeholder": "Your username",
#     "class": "w-full py-4 px-6 rounded-xl"
# }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your username",
                "class": INPUT_CLASSES,
            }
        )
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your password",
                "class": INPUT_CLASSES,
            }
        )
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": INPUT_CLASSES,
            }
        )
    )
