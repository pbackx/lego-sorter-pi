import asyncio
import base64
from contextlib import asynccontextmanager
import cv2
from fastapi import FastAPI, WebSocket
from picamera2 import Picamera2, Preview
import time
import traceback

from model.websocket_response import WebSocketResponse

picam2: Picamera2 = None
active_connections: list[WebSocket] = []


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
            img_bytes = bytes(cv2.imencode('.jpg', img_rgb)[1])
            img_encoded = base64.b64encode(img_bytes).decode('ascii')
            websocket_response = WebSocketResponse(image=img_encoded)
            
            for websocket in active_connections:
                await websocket.send_json(websocket_response.model_dump())
            await asyncio.sleep(0.03)  # 30 FPS
        except asyncio.CancelledError:
            return
        except:
            print("Camera error:")
            traceback.print_exc()
            stopped = True


class CameraManger:
    def __init__(self):
        self.camera_send_task: asyncio.Task = None
    
    def add_listener(self, websocket: WebSocket):
        active_connections.append(websocket)
        if not self.camera_send_task:
            print("Starting camera sender")
            self.camera_send_task = asyncio.create_task(send_camera())
    
    def remove_listener(self, websocket: WebSocket):
        if websocket in active_connections:
            active_connections.remove(websocket)
            if len(active_connections) == 0 and self.camera_send_task:
                print("Stopping camera sender")
                self.camera_send_task.cancel()
                self.camera_send_task = None


_camera_manager_instance = CameraManger()

async def get_camera_manager() -> CameraManger:
    return _camera_manager_instance