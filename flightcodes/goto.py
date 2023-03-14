#!/usr/bin/env python3

import asyncio
from mavsdk import System
import time

async def run():
    point1=(39.8724247,32.7347280)
    point2=(39.8723196,32.7347082)
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:921600")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_positon_ok abd health.is_home_position_ok:
            print(f"-- Global position state is good enough!")
            break    

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

    print("-- Arming")
    await drone.action.arm()

    await drone.action.set_takeoff_altitude(5)
    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(1)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 5
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(point1[0],point1[1], flying_alt, 0)
    await asyncio.sleep(5)
    await drone.action.goto_location(point2[0],point2[1], flying_alt, 0)
    while True:
        print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())



'''
    async for health in drone.telemetry.health():
        print(health)
        if health.is_global_position_ok and health.is_home_position_ok:
            print(f"-- Global position state is good enough!")
            break   
'''
    async for gps_info in drone.telemetry.position():
        print(gps_info)
        
