from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("tasks.urls")),
    path("user/", include("signup.urls")),
    path("admin/", admin.site.urls),
]
