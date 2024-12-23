import asyncio
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
from lib.predict import BrickognizeModelPrediction


app = FastAPI(lifespan=camera_lifespan)

predict_method = BrickognizeModelPrediction()

bucket_mapping = {
  "2780": 0,
  "4459": 0,
  "3673": 0,
}
default_bucket = 1


@app.websocket("/stream")
async def video_stream(
    websocket: WebSocket, 
    camera_manager: CameraManager = Depends(get_camera_manager),
    motor_control: MotorControl = Depends(get_motor_control),
    brick_detector: BrickDetector = Depends(get_brick_detector)):

    await websocket.accept()
    machine_running = False
    machine_task: asyncio.Task = None

    async def run_machine():
        stopped = False
        while not stopped:
            try:
                #TODO should put this in a thread so it can be aborted right away
                filename = await brick_detector.next_brick(ref_image_listener, threshold_image_listener)
                prediction = predict_method(filename)
                predicted_confidence = prediction["confidence"]
                predicted_brick_type = str(prediction["prediction"])
                bucket = bucket_mapping[predicted_brick_type] if predicted_brick_type in bucket_mapping and predicted_confidence > 0.85 else default_bucket
                print(f'{predicted_brick_type} predicted with score {predicted_confidence}, storing in bucket {bucket}')
                motor_control.move_turntable(bucket)
                await asyncio.sleep(6) # wait for bucket to be in position
                motor_control.clear_camera_belt()
                await asyncio.sleep(6) # wait for belt to clear
            except:
                print("Error during machine run")
                traceback.print_exc()
                stopped = True

    async def ref_image_listener(ref_image: np.ndarray):
        try:
            websocket_response = WebSocketResponse(referenceImage=base64_encode_jpg(ref_image), machineRunning=machine_running)
            await websocket.send_json(websocket_response.model_dump())
        except:
            print("Error sending ref image")
            traceback.print_exc()
    
    async def threshold_image_listener(image: np.ndarray):
        try:
            websocket_response = WebSocketResponse(thresholdImage=base64_encode_jpg(image), machineRunning=machine_running)
            await websocket.send_json(websocket_response.model_dump())
        except:
            print("Error sending threshold image")
            traceback.print_exc()

    async def camera_listener(img: np.ndarray):
        try:
            websocket_response = WebSocketResponse(image=base64_encode_jpg(img), machineRunning=machine_running)
            await websocket.send_json(websocket_response.model_dump())
        except:
            print("Ignoring exception while sending image to websocket")
            # TODO deregister camera_listener when connection is closed

    async def send_status(response: WebSocketResponse = WebSocketResponse(machineRunning=machine_running)):
        try:
            await websocket.send_json(response.model_dump())
        except:
            print("Exception while sending status.")
            traceback.print_exc()

    try:    
        while True:
            data = await websocket.receive_json()
            request = WebSocketRequest(**data)

            if request.streamCamera is not None:
                if request.streamCamera:
                    camera_manager.add_listener(camera_listener)
                else:
                    camera_manager.remove_listener(camera_listener)

            if request.bucket is not None:
                print(f"Changing to bucket {request.bucket}")
                motor_control.move_turntable(request.bucket)

            if request.clearBelt:
                if machine_running:
                    pass
                machine_running = True
                motor_control.clear_camera_belt()
                await send_status()
                await asyncio.sleep(3)
                machine_running = False
                await send_status()

            if request.makeReferenceImage:
                print("Creating new reference image")
                ref_img = await brick_detector.make_new_reference_image()
                await ref_image_listener(ref_img)

            if request.nextBrick:
                if machine_running:
                    pass
                machine_running = True
                print("Next brick")
                filename = await brick_detector.next_brick(ref_image_listener, threshold_image_listener)
                print(f"Stored in {filename}")
                machine_running = False
                await send_status()

            if request.predictOne:
                if machine_running:
                    pass
                machine_running = True
                print("Predicting one brick")
                filename = await brick_detector.next_brick(ref_image_listener, threshold_image_listener)
                prediction = predict_method(filename)
                machine_running = False
                await send_status(WebSocketResponse(prediction=prediction["prediction"], machineRunning=machine_running))

            if request.stop:
                if machine_task:
                    machine_task.cancel()
                brick_detector.stop()
                motor_control.stop_all()
                machine_running = False
                await send_status()

            if request.start:
                machine_running = True
                machine_task = asyncio.create_task(run_machine())


    except WebSocketDisconnect:
        print("Client disconnected")
