
import asyncio
from mavsdk import System

#point2[0] -> enlem
#point2[1] -> boylam
async def run():

    point1=(39.8734940,32.7304986)
    point2=(39.8733330,32.7303005)
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:460800")

   
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
    await drone.action.set_takeoff_altitude(5)
    await drone.action.takeoff()
    print("point1")
    await asyncio.sleep(10)
    print("kalkti")
    flying_alt = absolute_altitude + 5.0
    await drone.action.goto_location(point1[0],point1[1],flying_alt,0)
    await asyncio.sleep(15)
    print("1egidildi")
    await drone.action.goto_location(point2[0],point2[1],flying_alt,225)
    await asyncio.sleep(10)
    print("2yegidildi")
    print("-- Landing")
    await drone.action.land()





if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

