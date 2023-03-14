
import asyncio
from mavsdk import System


async def run():

    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:460800")


    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    print("gps")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("ok")
            break

    print("-- Arming")
    await drone.action.arm()
    await drone.action.set_takeoff_altitude(5)
    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()






if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
