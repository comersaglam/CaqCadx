from django.urls import path
from . import views   # import views from the same app

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
]
