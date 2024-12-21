#!/usr/bin/env bash

pushd api
.venv/bin/datamodel-codegen --input ../schema/websocket/request.json --input-file-type jsonschema --output model/websocket_request.py
.venv/bin/datamodel-codegen --input ../schema/websocket/response.json --input-file-type jsonschema --output model/websocket_response.py
popd

pushd ui
npx json-schema-to-zod -i ../schema/websocket/request.json -o src/model/WebSocketRequest.ts
npx json-schema-to-zod -i ../schema/websocket/response.json -o src/model/WebSocketResponse.ts
popd
