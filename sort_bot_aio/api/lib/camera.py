import asyncio
import base64
from contextlib import asynccontextmanager
import cv2
from fastapi import FastAPI, WebSocket
from picamera2 import Picamera2, Preview
import time
import traceback
from typing import Awaitable, Callable
import numpy as np

from model.websocket_response import WebSocketResponse

CameraListener = Callable[[np.ndarray], Awaitable]

picam2: Picamera2 = None
active_listeners: list[CameraListener] = []


@asynccontextmanager
async def camera_lifespan(app: FastAPI):
    global picam2
    picam2 = Picamera2()
    # using the default configuration for now
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    # Start the preview and camera
    picam2.start_preview(Preview.NULL)
    picam2.start()
    print("Starting PiCam")
    time.sleep(2)
    picam2.set_controls({"ExposureValue": 1})
    yield
    picam2.stop()
    picam2.stop_preview()
    picam2.close()


async def send_camera():
    global picam2
    stopped = False
    while not stopped:
        try:
            img = picam2.capture_array("main")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            for listener in active_listeners:
                await listener(img_rgb)

            await asyncio.sleep(0.03)  # 30 FPS
        except asyncio.CancelledError:
            return
        except:
            print("Camera error:")
            traceback.print_exc()
            stopped = True


def websocket_listener(websocket: WebSocket) -> CameraListener:
    async def listener(img: np.ndarray):
        img_bytes = bytes(cv2.imencode('.jpg', img)[1])
        img_encoded = base64.b64encode(img_bytes).decode('ascii')
        websocket_response = WebSocketResponse(image=img_encoded)
        await websocket.send_json(websocket_response.model_dump())
    return listener


class CameraManager:
    def __init__(self):
        self.camera_send_task: asyncio.Task = None
        self.websocket_listeners: dict[WebSocket, CameraListener] = {}
    
    def add_websocket_listener(self, websocket: WebSocket):
        new_listener = websocket_listener(websocket)
        self.websocket_listeners[websocket] = new_listener
        self.add_listener(new_listener)
    
    def add_listener(self, listener: CameraListener) -> None:
        active_listeners.append(listener)
        if not self.camera_send_task:
            print("Starting camera sender")
            self.camera_send_task = asyncio.create_task(send_camera())
    
    def remove_websocket_listener(self, websocket: WebSocket):
        if websocket in self.websocket_listeners:
            listener = self.websocket_listeners.pop(websocket)
            self.remove_listener(listener)

    def remove_listener(self, listener: CameraListener) -> None:
        if listener in active_listeners:
            active_listeners.remove(listener)
            if len(active_listeners) == 0 and self.camera_send_task:
                print("Stopping camera sender")
                self.camera_send_task.cancel()
                self.camera_send_task = None
    


_camera_manager_instance = CameraManager()

def get_camera_manager() -> CameraManager:
    return _camera_manager_instance