"""
URL configuration for CaqCadx project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),   # core app
    path("labeling/", include("labeling.urls")),  # labeling app
    path("payments/", include("payments.urls")),  # payments app
    path("accounts/", include("allauth.urls")),   # django-allauth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
