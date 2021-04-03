#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def hello(websocket, path):
    while True:
        name = await websocket.recv()
        # print(f"< {name}")
        file = open('ESP32_CAM_Real.jpg','wb')
        file.write(name)
        file.close()

    # greeting = f"Hello {name}!"
    # await websocket.send(greeting)
    # print(f"> {greeting}")


# start_server = websockets.serve(hello, "localhost", 8888)
start_server = websockets.serve(hello, "10.0.0.12", 8888)

print("----------RUN-----------")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
