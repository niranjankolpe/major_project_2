from django.shortcuts import render, redirect
from django.conf import settings

from detector_app.mango_fruit_detection import *

# Create your views here.
def index(request):
    return redirect("home")

def home(request):
    read_text = ""
    with open("media_files/models/sample_text_model.txt", "r") as model:
        read_text = " ".join(model.readlines())
    context = {'media_url': settings.MEDIA_URL, 'read_text': read_text}
    return render(request, "detector_app/index.html", context)

def detector(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/detector.html", context)

def start_detection(request):
    detector = MangoDetection()
    detector()
    return redirect("home")