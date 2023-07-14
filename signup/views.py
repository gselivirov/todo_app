from django.shortcuts import render
from django.views import View
from .forms import SignupForm

class SignupView(View):
    form_class = SignupForm
    # def post(self, request, *args, **kwargs):
        

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, "signup/signup.html", {"form": form})


# class LoginView(View):
#     def post(self, request, *args, **kwargs):
#         return

#     def get(self, request, *args, **kwargs):
#         return render(request, "signup/login.html", {})
