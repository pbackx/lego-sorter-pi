import os
from datetime import datetime

from flask import Flask, request
import predict_brick

app = Flask(__name__)
base_dir = 'C:\\dev\\lego-sorter-pi\\data\\new'
temp_file = 'C:\\dev\\lego-sorter-pi\\data\\tmp\\img.jpg'

@app.route("/predict", methods=['POST'])
def predict():
    image = request.files['image']
    image.save(temp_file)
    label = predict_brick.predict(temp_file)

    labeled_dir = f'{base_dir}\\{label}'
    os.makedirs(labeled_dir, exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    os.rename(temp_file, f'{labeled_dir}\\{filename}')

    return {
        "prediction": label
    }
