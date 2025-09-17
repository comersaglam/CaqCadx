from django.urls import path
from . import views

app_name = "labeling"

urlpatterns = [
    path("annotate/", views.annotate, name="annotate"),
    path("start/", views.start, name="start"),
]
