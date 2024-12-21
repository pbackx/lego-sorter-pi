import numpy as np
from .camera import get_camera_manager

class BrickDetector:
    def __init__(self) -> None:
        self.reference_image: np.ndarray = None
        self.camera_manager = get_camera_manager()

    def make_new_reference_image(self) -> None:
        self.camera_manager.add_listener(self._internal_make_new_reference_image)

    async def _internal_make_new_reference_image(self, image:np.ndarray) -> None:
        print("making new ref image")
        self.camera_manager.remove_listener(self._internal_make_new_reference_image)

_brick_detector_instance = BrickDetector()

async def get_brick_detector() -> BrickDetector:
    return _brick_detector_instance