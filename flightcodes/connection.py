
import asyncio
from mavsdk import System
import time

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:460800")

    await drone.telemetry.set_rate_gps_info(3.0)

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    print("Waiting for drone to have a global position estimate...")
  #  async for terrain_info in drone.telemetry.home():
  #      print(terrain_info)
  #  asyncio.ensure_future(print_terrain(drone))
    
  #  asyncio.ensure_future(print_battery(drone))

    while True:

        asyncio.ensure_future(print_gps_info(drone)) 
    #    asyncio.ensure_future(print_terrain(drone))
        #print("Staying connected, press Ctrl-C to exit")
        await asyncio.sleep(1)

async def print_terrain(drone):
    async for terrain_info in drone.telemetry.health():
        print(terrain_info)
async def print_gps_info(drone):
    print("a")
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")
async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")
        await asyncio.sleep(1.7)
async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
