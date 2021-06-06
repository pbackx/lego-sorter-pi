import cv2 as cv
from keras.models import load_model
from matplotlib import pyplot as plt
import numpy as np
import preprocess_lego_image
from os import listdir
from tensorflow.keras.applications.vgg16 import preprocess_input
import tensorflow as tf

model = load_model('model')
data_dir_labeled = '..\\data\\labeled'
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