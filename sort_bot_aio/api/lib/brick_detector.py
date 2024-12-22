import asyncio
from typing import Awaitable, Callable
import cv2
import numpy as np
from .camera import get_camera_manager

ReferenceImageListener = Callable[[np.ndarray], Awaitable]

class BrickDetector:
    top_border = 100
    bottom_border = 40

    def __init__(self) -> None:
        self.reference_image: np.ndarray = None
        self.camera_manager = get_camera_manager()
        self.reference_image_listener: ReferenceImageListener = lambda _: None

    def make_new_reference_image(self, listener: ReferenceImageListener = lambda _: None) -> None:
        self.reference_image_listener = listener
        self.camera_manager.add_listener(self._internal_make_new_reference_image)

    def _pre_process_image(self, image: np.ndarray) -> np.ndarray:
        without_borders = image[self.top_border:480-self.bottom_border,:]
        gray = cv2.cvtColor(without_borders, cv2.COLOR_RGB2GRAY)
        return cv2.GaussianBlur(gray, (21, 21), 0)

    async def _internal_make_new_reference_image(self, image:np.ndarray) -> None:
        print("Making new ref image")
        self.reference_image = self._pre_process_image(image)
        self.camera_manager.remove_listener(self._internal_make_new_reference_image)
        await self.reference_image_listener(self.reference_image)

_brick_detector_instance = BrickDetector()

async def get_brick_detector() -> BrickDetector:
    return _brick_detector_instance