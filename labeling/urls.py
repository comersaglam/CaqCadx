from django.urls import path
from . import views

app_name = "labeling"

urlpatterns = [
    path("start/", views.start, name="start"),
]
