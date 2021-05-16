from flask import Flask, request
import predict_brick

app = Flask(__name__)


@app.route("/predict", methods=['POST'])
def predict():
    image = request.files['image']
    image.save('C:\\dev\\lego-sorter-pi\\data\\tmp\\img.jpg')
    return {
        "prediction": predict_brick.predict('C:\\dev\\lego-sorter-pi\\data\\tmp\\img.jpg')
    }
