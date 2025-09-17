from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
@login_required
def start(request):
    return render(request, "labeling/start.html")


import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Exists, OuterRef
from .models import ImageItem, Annotation


@login_required
def annotate(request):
    """Main annotation page: show next image or save submitted labels."""

    # --- Handle form submission ---
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        image = get_object_or_404(ImageItem, pk=image_id)

        # Create or update annotation
        ann, _ = Annotation.objects.get_or_create(
            image=image,
            user=request.user,
        )

        # Depending on is_cut, save correct fields
        if image.is_cut:
            ann.localization_label = request.POST.get("localization_label", -1)
            ann.size_label = request.POST.get("size_label", -1)
            ann.cleanliness_label = request.POST.get("cleanliness_label", -1)
            ann.overall = request.POST.get("overall", -1)
        else:
            ann.colonexpansion_label = request.POST.get("colonexpansion_label", -1)
            ann.img_cleanliness = request.POST.get("img_cleanliness", -1)
            ann.img_overall = request.POST.get("img_overall", -1)

        ann.save()

        # Redirect to get next image
        return redirect("labeling:annotate")

    # --- Select next image ---
    # All images not yet annotated by this user
    annotated = Annotation.objects.filter(user=request.user, image=OuterRef("pk"))
    candidates = ImageItem.objects.annotate(
        already=Exists(annotated)
    ).filter(already=False)

    image = candidates.order_by("?").first()  # pick random one

    if not image:
        return render(request, "labeling/done.html")  # no more images

    #return render(request, "labeling/annotate.html", {"image": image})

    return render(request, "labeling/annotate.html", {
        "image": image,
        "MEDIA_URL": settings.MEDIA_URL,  # 👈 extra context variable
    })

