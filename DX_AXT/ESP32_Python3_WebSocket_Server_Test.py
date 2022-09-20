#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def hello1(websocket, path):
    while True:
        recv_str  = await websocket.recv()
        # print(f"< {name}")
        # print("p1")
        file = open('ESP32_CAM_Real.jpg','wb')
        file.write(recv_str)
        file.close()

    # greeting = f"Hello {name}!"
    # await websocket.send(greeting)
    # print(f"> {greeting}")

async def hello2(websocket, path):
    while True:
        name1 = await websocket.recv()
        # print(f"< {name}")
        # print("p2")
        file1 = open('ESP32_CAM_Real.jpg','wb')
        file1.write(name1)
        file1.close()


# start_server = websockets.serve(hello, "localhost", 8888)
start_server1 = websockets.serve(hello1, "10.0.0.15", 8888)
start_server2 = websockets.serve(hello2, "10.0.0.15", 8886)
# start_server1 = websockets.serve(hello1, "192.168.31.188", 8888)
# start_server2 = websockets.serve(hello2, "192.168.31.188", 8886)

print("----------RUN-----------")
asyncio.get_event_loop().run_until_complete(start_server1)
asyncio.get_event_loop().run_until_complete(start_server2)
asyncio.get_event_loop().run_forever()
