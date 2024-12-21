This folder contains an all-in-one solution for running the Lego sorter. It consists of a server running on
the Raspberry Pi with a graphical front-end that you can open in any browser.

For development, run this as two servers:
1. FastAPI Python API server that the UI will connect to over websocket
2. Vite React application for the frontend that connects to the API server via websocket

# Generating the schema

Communication on the websocket is governed by the schema defined in the schema folder. This schema is converted
into Pydantic and TypeScript objects that are used by respecitevly the API server and the UI frontend.

For Pydantic:

    cd api
    mkdir model
    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate
    pip install -r requirements.txt -r requirements.dev.txt
    datamodel-codegen --input ../schema/websocket/request.json --input-file-type jsonschema --output model/websocket_request.py
    datamodel-codegen --input ../schema/websocket/response.json --input-file-type jsonschema --output model/websocket_response.py

For TypeScript:

    cd ui
    mkdir src/model
    npm install
    npx json-schema-to-zod -i ../schema/websocket/request.json -o src/model/WebSocketRequest.ts
    npx json-schema-to-zod -i ../schema/websocket/response.json -o src/model/WebSocketResponse.ts


# API server

In the API folder, initialize a virtual environment based on the OS packages (this is important to be able to
access picam2 and a properly compiled OpenCV)

    cd api
    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Start the server:

    fastapi dev

# UI

    cd ui
    npm install
    npm run dev

The UI should now be accessible on http://localhost:5173
