import cv2 as cv

margin = int((640-480)/2)

def preprocess(image_path):
    image = cv.imread(image_path)
    cropped = image[:, margin:-margin]
    return cv.resize(cropped, (256,256), interpolation=cv.INTER_AREA)