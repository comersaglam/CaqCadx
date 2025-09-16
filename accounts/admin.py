from django.contrib import admin
from .models import AllowedEmail

# Register your models here.

@admin.register(AllowedEmail)
class AllowedEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "active", "note")
    list_filter = ("active",)
    search_fields = ("email",)
