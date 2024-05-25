import os
import predict_brick
import shutil
from fastapi import FastAPI, UploadFile, File

app = FastAPI()
temp_folder = "/new_pictures"

@app.post("/predict")
def predict(image: UploadFile = File(...)):
    image_file = os.path.join(temp_folder, image.filename)
    with open(image_file, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    label, confidence = predict_brick.predict(image_file)

    return {
        "prediction": label,
        "confidence": float(confidence)
    }