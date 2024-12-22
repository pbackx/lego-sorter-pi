import asyncio
from typing import Awaitable, Callable
import cv2
import numpy as np
from .camera import CameraManager, get_camera_manager
from .motor_control import get_motor_control, MotorControl

BrickDetectorImageListener = Callable[[np.ndarray], Awaitable]

class BrickDetector:
    top_border = 100
    bottom_border = 40

    def __init__(self) -> None:
        self.reference_image: np.ndarray = None
        self.camera_manager: CameraManager = get_camera_manager()
        self.motor_control: MotorControl = get_motor_control()
        self.threshold_image_listener: BrickDetectorImageListener = lambda _: None

    async def make_new_reference_image(self) -> np.ndarray:
        image = await self.camera_manager.take_single_picture()
        self.reference_image = self._pre_process_image(image)
        return self.reference_image

    def _pre_process_image(self, image: np.ndarray) -> np.ndarray:
        without_borders = image[self.top_border:480-self.bottom_border,:]
        gray = cv2.cvtColor(without_borders, cv2.COLOR_RGB2GRAY)
        return cv2.GaussianBlur(gray, (21, 21), 0)
    
    def stop(self):
        self.camera_manager.remove_listener(self._internal_next_brick)
        self.motor_control.stop_all()

    async def next_brick(
            self, 
            listener: BrickDetectorImageListener = lambda _: None,
            treshold_listener: BrickDetectorImageListener = lambda _: None
        ) -> None:
        self.threshold_image_listener = treshold_listener
        if self.reference_image is None:
            await self.make_new_reference_image()
            await listener(self.reference_image)
        self.camera_manager.add_listener(self._internal_next_brick)
        self.motor_control.on_all()

    async def _update_threshold_image(self, image: np.ndarray) -> int:
        gray = self._pre_process_image(image)
    
        image_diff = cv2.absdiff(self.reference_image, gray)
        thresh = cv2.threshold(image_diff, 50, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        left_most_contour_x = 640
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 40:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            if w > 600 or w < 50:
                continue
            # cv2.rectangle(cam_img, (x, y + top_border), (x + w, y + h + top_border), (0, 255, 0), 2)
            if x < left_most_contour_x:
                left_most_contour_x = x 

        await self.threshold_image_listener(thresh)
        return left_most_contour_x

    async def _internal_next_brick(self, image: np.ndarray):
        contour_x = await self._update_threshold_image(image)

        if contour_x < 640:
            self.camera_manager.remove_listener(self._internal_next_brick)
            self.motor_control.stop_all()
            await asyncio.sleep(0.5)


_brick_detector_instance = BrickDetector()

async def get_brick_detector() -> BrickDetector:
    return _brick_detector_instance