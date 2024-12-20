import time
from fastapi import Depends, FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from camera import camera_lifespan, CameraManger, get_camera_manager


app = FastAPI(lifespan=camera_lifespan)


@app.websocket("/stream")
async def video_stream(websocket: WebSocket, camera_manager: CameraManger = Depends(get_camera_manager)):
    await websocket.accept()

    try:    
        while True:
            data = await websocket.receive_json()
            stream_camera = data['streamCamera']

            if stream_camera:
                camera_manager.add_listener(websocket)
            else:
                camera_manager.remove_listener(websocket)


    except WebSocketDisconnect:
        print("Client disconnected")
