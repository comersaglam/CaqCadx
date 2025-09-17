from django.contrib import admin
from .models import ImageItem, Annotation


class AnnotationInline(admin.TabularInline):  # or StackedInline if you prefer big forms
    model = Annotation
    extra = 0   # don’t show empty extra rows by default
    readonly_fields = ("user", "created_at")  # optional: make some fields readonly

from django.contrib import admin
from .models import ImageItem, Annotation


class AnnotationInline(admin.TabularInline):
    model = Annotation
    extra = 0


@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    # show all fields of ImageItem
    list_display = [field.name for field in ImageItem._meta.get_fields() if not field.many_to_many and not field.one_to_many]
    inlines = [AnnotationInline]
    search_fields = [field.name for field in ImageItem._meta.get_fields() if field.get_internal_type() in ("CharField", "TextField")]


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    # show all fields of Annotation
    list_display = [field.name for field in Annotation._meta.get_fields() if not field.many_to_many and not field.one_to_many]
    search_fields = [field.name for field in Annotation._meta.get_fields() if field.get_internal_type() in ("CharField", "TextField")]


"""@admin.register(ImageItem)
class ImageItemAdmin(admin.ModelAdmin):
    list_display = ("id", "path", "is_polyp", "is_cut", "size", "pathology_diagnosis")
    list_filter = ("is_polyp", "is_cut", "pathology_diagnosis")
    search_fields = ("path", "size", "pathology_diagnosis")
    inlines = [AnnotationInline]   # <-- show annotations inline


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "user", "overall", "created_at")
    list_filter = ("overall", "created_at")
    search_fields = ("image__path", "user__username")
"""