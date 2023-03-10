
import asyncio
from mavsdk import System

point1=(39.8734940,32.7304986)
point2=(39.8733330,32.7303005)
#point2[0] -> enlem
#point2[1] -> boylam
async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

    print("-- Arming")
    
    
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)
    flying_alt = absolute_altitude + 5.0
    await drone.action.goto_location(point1[0],point1[1],flying_alt,0)
    await asyncio.sleep(5)    

    await drone.action.goto_location(point2[0],point2[1],flying_alt,0)
    await asyncio.sleep(5)    

    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()



async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

