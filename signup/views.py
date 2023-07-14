from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm


class SignupView(View):
    form_class = SignupForm
    template_name = "signup/signup.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})


# class LoginView(View):
#     def post(self, request, *args, **kwargs):
#         return

#     def get(self, request, *args, **kwargs):
#         return render(request, "signup/login.html", {})
