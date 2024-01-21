from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
def index(request):
    return redirect("home")

def home(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/index.html", context)
