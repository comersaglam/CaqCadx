from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def start(request):
    return render(request, "labeling/start.html")
