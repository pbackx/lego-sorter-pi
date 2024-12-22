import time
import traceback
from fastapi import Depends, FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from lib.brick_detector import BrickDetector, get_brick_detector
from lib.camera import camera_lifespan, CameraManager, get_camera_manager
from lib.motor_control import get_motor_control, MotorControl
from model.websocket_request import WebSocketRequest
import numpy as np

from model.websocket_response import WebSocketResponse
from lib.tools import base64_encode_jpg


app = FastAPI(lifespan=camera_lifespan)


@app.websocket("/stream")
async def video_stream(
    websocket: WebSocket, 
    camera_manager: CameraManager = Depends(get_camera_manager),
    motor_control: MotorControl = Depends(get_motor_control),
    brick_detector: BrickDetector = Depends(get_brick_detector)):

    await websocket.accept()

    async def ref_image_listener(ref_image: np.ndarray):
        try:
            websocket_response = WebSocketResponse(referenceImage=base64_encode_jpg(ref_image))
            await websocket.send_json(websocket_response.model_dump())
        except:
            print("Error sending ref image")
            traceback.print_exc()
    
    async def threshold_image_listener(image: np.ndarray):
        try:
            websocket_response = WebSocketResponse(thresholdImage=base64_encode_jpg(image))
            await websocket.send_json(websocket_response.model_dump())
        except:
            print("Error sending threshold image")
            traceback.print_exc()

    try:    
        while True:
            data = await websocket.receive_json()
            request = WebSocketRequest(**data)

            if request.streamCamera is not None:
                if request.streamCamera:
                    camera_manager.add_websocket_listener(websocket)
                else:
                    camera_manager.remove_websocket_listener(websocket)

            if request.bucket is not None:
                print(f"Changing to bucket {request.bucket}")
                motor_control.move_turntable(request.bucket)

            if request.clearBelt:
                motor_control.clear_camera_belt()

            if request.makeReferenceImage:
                print("Creating new reference image")
                ref_img = await brick_detector.make_new_reference_image()
                await ref_image_listener(ref_img)

            if request.nextBrick:
                print("Next brick")
                await brick_detector.next_brick(ref_image_listener, threshold_image_listener)

            if request.stop:
                brick_detector.stop()
                motor_control.stop_all()


    except WebSocketDisconnect:
        print("Client disconnected")
