import time
from fastapi import Depends, FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from lib.brick_detector import BrickDetector, get_brick_detector
from lib.camera import camera_lifespan, CameraManager, get_camera_manager
from lib.motor_control import get_motor_control, MotorControl
from model.websocket_request import WebSocketRequest


app = FastAPI(lifespan=camera_lifespan)


@app.websocket("/stream")
async def video_stream(
    websocket: WebSocket, 
    camera_manager: CameraManager = Depends(get_camera_manager),
    motor_control: MotorControl = Depends(get_motor_control),
    brick_detector: BrickDetector = Depends(get_brick_detector)):

    await websocket.accept()

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
                brick_detector.make_new_reference_image()



    except WebSocketDisconnect:
        print("Client disconnected")
