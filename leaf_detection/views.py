from django.shortcuts import render, redirect
from django.conf import settings

import tensorflow as tf
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np

import traceback

# Create your views here.
def leaf_detector(request):
    context = {'media_url': settings.MEDIA_URL}
    return render(request, "leaf_detection/index.html", context)

def get_class_prediction(predictions):
    class_names = ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould']
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
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
            predicted_class = get_class_prediction(predictions)  # Get the predicted class label
            predicted_class = str(predicted_class)
        except Exception:
            predicted_class = f"Error! {Exception}"
            print()
            traceback.print_exc()
            print()
            
    else:
        return redirect("home")
    context = {'predicted_class': predicted_class, 'media_url': settings.MEDIA_URL}
    return render(request, "leaf_detection/result.html", context)