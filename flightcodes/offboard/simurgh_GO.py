
import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


async def run():
    """ Does Offboard control using position NED coordinates. """

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

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    
    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Go 0m North, 0m East, -5m Down within local coordinate system")
    task1=asyncio.create_task(drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0,-7.0, 0.0)))
    await task1
    print("-- Go 5m North within local coordinate system, <<N>>")
    task2=asyncio.create_task(drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, 0.0, 0)))
    await task2
    print("-- Go 5m East within local coordinate system, <<N>>")
  
    task3=asyncio.create_task(drone.offboard.set_position_ned(PositionNedYaw(0.0, 5.0, 0.0, 0)))
    await task3
    print("-- Go 5m South within local coordinate system, <<N>>")
    task4=asyncio.create_task(drone.offboard.set_position_ned(PositionNedYaw(-5.0, 0.0, 0.0, 0)))
    await task4
    print("-- Go 5m West within local coordinate system, <<N>>")
     
    task5=asyncio.create_task(drone.offboard.set_position_ned(PositionNedYaw(0.0, -5.0, 0.0, 0)))
    await task5
    print("-- Go -5m Down within local coordinate system, <<N>>")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 5.0, 0.0))
    await asyncio.sleep(10)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
