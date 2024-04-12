from django.shortcuts import render, redirect
from django.conf import settings

import cv2
from detector_app.mango_fruit_detection import *
import tensorflow as tf
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np

import matplotlib.pyplot as plt
import traceback

# Create your views here.

def index(request):
    return redirect("home")

def home(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/home.html", context)

def detector(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/mango_classifier.html", context)

def homemade_remedies(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/homemade_remedies.html", context)

def image_classify(request):
    predicted_class = ""
    detector = MangoDetection()
    detector()
    if request.method == "POST":
        try:
            file_object = request.FILES["mango_chi_image"]
            file_name = str(file_object)
            save_file_path = f"temporary_storage/{file_name}"
            with open(save_file_path, 'wb+') as f:
                for chunk in file_object.chunks():
                    f.write(chunk)
            print(file_name)
            image = cv2.imread(save_file_path)
            output_image = detector.classify_mango_image(image)
            cv2.imshow("Mango Object Detection and Classification", output_image)
            cv2.waitKey(0)
            cv2.imwrite(f"output_images/{file_name}", output_image)
            print("\n\nImage saved!")
        except Exception:
            predicted_class = f"Error! {Exception}"
            print()
            traceback.print_exc()
            print() 
    else:
        return redirect("home")
    context = {'predicted_class': predicted_class, 'media_url': settings.MEDIA_URL}
    return render(request, "detector_app/home.html", context)

def start_detection(request):
    detector = MangoDetection()
    detector()
    if request.method == "GET":
        detector.live_detection()
    return redirect("home")