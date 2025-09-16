"""
URL configuration for CaqCadx project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # Include URLs from the core app,
    path("labeling/", include("labeling.urls")), # Include URLs from the labeling app
    path("payments/", include("payments.urls")), # Include URLs from the payments app
    path("accounts/", include("allauth.urls")), # Include URLs from the allauth app
    #path("accounts/", include("accounts.urls")), # Include URLs from the accounts app
]
