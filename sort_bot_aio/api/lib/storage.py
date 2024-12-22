import cv2
from datetime import datetime
import numpy as np
import os

class DataStorage:
    def __init__(self, prefix = ''):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(current_folder, '../../../data/new')
        self.prefix = prefix

    def store_jpg(self, image_array: np.ndarray) -> str:
        filename = os.path.join(self.data_path, self.prefix + datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg")
        image_jpg_bytes = bytes(cv2.imencode('.jpg', image_array)[1])
        with open(filename, "wb") as file:
            file.write(image_jpg_bytes)
        return filename

def get_storage(): 
    return DataStorage()