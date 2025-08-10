import copy
import json
import math
import time
import uuid
from pprint import pprint
import websockets
import asyncio
import os
import glob


connected = set()


async def send_data(websocket):
    res = {}
    # 数据发送到前端
    await websocket.send(json.dumps(res))


async def handle_message(websocket, message):
    print(message)
    if message == "begin":
        connected.add(websocket)
        asyncio.create_task(send_data(websocket))
    else:
        print('else')
        await websocket.send("get message: " + message + '但并非系统制定指令')


async def server(websocket):
    try:
        async for message in websocket:
            await handle_message(websocket, message)
    finally:
        connected.remove(websocket)


async def main():
    print("WebSocket服务器启动成功，端口号为8765")
    async with websockets.serve(server, "localhost", 8765):
        # async with websockets.serve(server, "0.0.0.0", 8765):
        await asyncio.Future()  # 保持运行


if __name__ == "__main__":
    asyncio.run(main())