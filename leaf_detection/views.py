from django.shortcuts import render, redirect
from django.conf import settings

import tensorflow as tf
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np

import traceback

# Create your views here.
def leaf_classifier_home(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "leaf_detection/leaf_classifier_home.html", context)

def get_class_prediction(predictions):
    class_names = ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould']
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    if predicted_class == "Anthracnose":
        return predicted_class, "Anthracnose.html"
    elif predicted_class == "Bacterial Canker":
        return predicted_class,"Bacterial_Canker.html"
    elif predicted_class == "Cutting Weevil":
        return predicted_class,"Cutting_Weevil.html"
    elif predicted_class == "Die Back":
        return predicted_class,"Die_Back.html"
    elif predicted_class == "Gall Midge":
        return predicted_class,"Gall_Midge.html"
    elif predicted_class == "Healthy":
        return predicted_class,"Healthy.html"
    elif predicted_class == "Powdery Mildew":
        return predicted_class,"Powdery_Mildew.html"
    elif predicted_class == "Sooty Mould":
        return predicted_class,"Sooty_Mould.html"
    return predicted_class

def import_and_predict(image):
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    img = np.asarray(image)
    img_reshape = img[np.newaxis, ...]
    model = tf.keras.models.load_model('media_files/models/mango_model.h5')
    prediction = model.predict(img_reshape)
    return prediction

def leaf_result(request):
    if request.method == "POST":
        try:
            image = Image.open(BytesIO(request.FILES['file'].read()))
            predictions = import_and_predict(image)
            predicted_class, output_page = get_class_prediction(predictions)  # Get the predicted class label
            predicted_class = str(predicted_class)
        except Exception:
            predicted_class = f"Error! {Exception}"
            print()
            traceback.print_exc()
            print()
    else:
        return redirect("home")
    context = {'predicted_class': predicted_class, 'media_url': settings.MEDIA_URL}
    return render(request, f"leaf_detection/{output_page}", context)