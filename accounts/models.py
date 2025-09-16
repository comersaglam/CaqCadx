from django.db import models

# Create your models here.
class AllowedEmail(models.Model):
    email = models.EmailField(unique=True)
    note = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email