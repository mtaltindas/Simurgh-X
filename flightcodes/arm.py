#!/usr/bin/env python3

import asyncio
from mavsdk import System
import time

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:460800")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("-- Arming")
    await drone.action.arm()
    time.sleep(2)
    await drone.action.disarm()
    while True:
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
