import base64
import cv2
import numpy as np

def base64_encode_jpg(image: np.ndarray) -> str:
    img_bytes = bytes(cv2.imencode('.jpg', image)[1])
    return base64.b64encode(img_bytes).decode('ascii')
