from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
context = {'media_url': settings.MEDIA_URL}
  
def index(request):
    return redirect("home")

def home(request):
    return render(request, "detector_app/index.html", context)
