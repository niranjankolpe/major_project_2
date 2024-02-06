from flask import Flask, request, render_template
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Function to load the model
def load_model():
    model = tf.keras.models.load_model('mango_model.h5')
    return model

# Function to preprocess an input image and get predictions
def import_and_predict(image_data, model):
    size = (224, 224)
    image = Image.open(BytesIO(image_data.read()))
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img = np.asarray(image)
    img_reshape = img[np.newaxis, ...]
    prediction = model.predict(img_reshape)
    return prediction

# Function to get the predicted class label from probabilities
def get_class_prediction(predictions):
    class_names = ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould']
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    return predicted_class

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    model = load_model()
    predictions = import_and_predict(file, model)
    predicted_class = get_class_prediction(predictions)  # Get the predicted class label
    print(predicted_class)
    return render_template('result.html', prediction=predicted_class)  # Pass the class label to the template

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
