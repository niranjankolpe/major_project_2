from django.shortcuts import render, redirect
from django.conf import settings

# Create your views here.
def index(request):
    return redirect("home")

def home(request):
    read_text = ""
    with open("media_files/models/model.txt", "r") as model:
        read_text = " ".join(model.readlines())
    context = {'media_url': settings.MEDIA_URL, 'read_text': read_text}
    return render(request, "detector_app/index.html", context)
