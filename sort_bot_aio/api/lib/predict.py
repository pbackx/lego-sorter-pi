import json
import requests
from typing import Protocol, TypedDict

class PredictionResult(TypedDict):
    prediction: str
    confidence: float

def filename(filepath: str) -> str:
    return filepath[filepath.rindex('/')+1:]

class ModelPrediction(Protocol):
    def __call__(self, filepath: str) -> PredictionResult:
        pass

class SelfTrainedModelPrediction(ModelPrediction):
    def __init__(self, predict_url: str):
        self.predict_url = predict_url

    def __call__(self, filepath: str) -> PredictionResult:
        with open(filepath, 'rb') as file:
            files={
                'image': (filename(filepath), file, 'image/jpeg')
            }
            headers = {
                'Accept': 'application/json',
            }
            return requests.request("POST", self.predict_url, headers=headers, files=files).json()
        
class BrickognizeModelPrediction(ModelPrediction):
    predict_url = 'https://api.brickognize.com/predict/'

    def _brickognize_prediction(self, brickognize_prediction):
        if not brickognize_prediction['items']:
            return {}
        return max(brickognize_prediction['items'], key=lambda x: x['score'])

    def __call__(self, filepath: str) -> PredictionResult:
        with open(filepath, 'rb') as file:
            files = {
                'query_image': (filename(filepath), file, 'image/jpeg')
            }
            response = requests.post(self.predict_url, files=files)

            # Store JSON response alongside original image
            json_path = filepath[:filepath.rindex('.')] + '.json'
            with open(json_path, 'w') as f:
                json.dump(response.json(), f, indent=4)

            prediction = self._brickognize_prediction(response.json())

            if not prediction:
                return {
                    'prediction': 'unknown',
                    'confidence': 0
                }

            return {
                'confidence': prediction["score"],
                'prediction': prediction["id"]
            }