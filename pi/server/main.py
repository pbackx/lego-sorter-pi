from contextlib import asynccontextmanager
import cv2
from picamera2 import Picamera2, Preview
import time
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

def start_cam():
    # Start the camera as we have explained in `01_testing_the_camera` notebook
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
    return picam2

picam2 = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global picam2
    picam2 = start_cam()
    yield
    picam2.stop()
    picam2.stop_preview()
    picam2.close()


app = FastAPI(lifespan=lifespan)


@app.websocket("/stream")
async def video_stream(websocket: WebSocket):
    await websocket.accept()

    try:    
        while True:
            img = picam2.capture_array("main")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_bytes = bytes(cv2.imencode('.jpg', img_rgb)[1])
            
            await websocket.send_bytes(img_bytes)
            await asyncio.sleep(0.03)  # 30 FPS
    except WebSocketDisconnect:
        print("Client disconnected")
