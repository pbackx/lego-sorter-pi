from keras.models import load_model
import numpy as np
import preprocess_lego_image
from os import listdir
from tensorflow.keras.applications.vgg16 import preprocess_input

model = load_model('model.keras')
data_dir_labeled = '/data/labeled'
labels = listdir(data_dir_labeled)
labels.sort()


def predict(filename):
    image = preprocess_lego_image.preprocess(filename)
    vgg16_preprocessed = preprocess_input(np.array([image]))
    prediction = model.predict(vgg16_preprocessed)
    most_likely = np.argmax(prediction)
    confidence = prediction[0][most_likely]
    label = labels[most_likely]
    return label, confidence