from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupView
from .forms import LoginForm


app_name = "signup"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="signup/login.html",
            authentication_form=LoginForm,
        ),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
    ),
]
