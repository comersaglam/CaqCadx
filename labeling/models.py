from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class ImageItem(models.Model):
    # Stable identifiers
    patient_id = models.CharField(max_length=128, null=True, blank=True)
    polyp_id = models.CharField(max_length=128, null=True, blank=True)
    img_file_prefix = models.CharField(max_length=128, null=True, blank=True)


    # Relative path inside dataset (e.g. "polar/train_set/.../file.png")
    path = models.CharField(max_length=512)

    # Metadata from CSV
    polyp_pos_xywh = models.CharField(max_length=128, blank=True, null=True)
    size = models.CharField(max_length=64, blank=True, null=True)
    pathology_diagnosis = models.CharField(max_length=128, blank=True, null=True)

    # Flags
    is_polyp = models.BooleanField(default=True)
    is_cut   = models.BooleanField(default=False)

    # Annotation placeholders
    localization_label   = models.IntegerField(default=-1)
    size_label           = models.IntegerField(default=-1)
    cleanliness_label    = models.IntegerField(default=-1)
    overall              = models.IntegerField(default=-1)
    colonexpansion_label = models.IntegerField(default=-1)
    img_cleanliness      = models.IntegerField(default=-1)
    img_overall          = models.IntegerField(default=-1)

    annotator_mail = models.CharField(max_length=128, default="none")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicates based on stable identifiers
        unique_together = ("patient_id", "polyp_id", "img_file_prefix")

    def __str__(self):
        return f"{self.patient_id}/{self.polyp_id}/{self.img_file_prefix}"



class Annotation(models.Model):
    """
    One user’s annotation of one image.
    This lets multiple users annotate the same ImageItem independently.
    """
    image = models.ForeignKey(ImageItem, on_delete=models.CASCADE, related_name="annotations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="annotations")

    # Labels from the web form
    localization_label = models.IntegerField(default=-1)
    size_label = models.IntegerField(default=-1)
    cleanliness_label = models.IntegerField(default=-1)
    overall = models.IntegerField(default=-1)
    colonexpansion_label = models.IntegerField(default=-1)
    img_cleanliness = models.IntegerField(default=-1)
    img_overall = models.IntegerField(default=-1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("image", "user")]  # prevent duplicate annotations

    def __str__(self):
        return f"{self.user} → {self.image}"
