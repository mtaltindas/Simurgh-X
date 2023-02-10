from pymavlink import mavutil

# Start a connection listening to a UDP port
vehicle = mavutil.mavlink_connection('udpin:localhost:14551')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
vehicle.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (vehicle.target_system, vehicle.target_component))
def arm_disarm(armParam,vehicle):
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, armParam, 0, 0, 0, 0, 0, 0)

    msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)

def takeoff(altitudeParam,vehicle):
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component,
                                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 10)

    msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)

def move(xParam,yParam,zParam,vehicle):
    #zParam minus value for altitude increase
    typeMask=int(0b100111111000)
    vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, vehicle.target_system,vehicle.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
                                                                                    typeMask, xParam, yParam, zParam, 0, 0, 0, 0, 0, 0, 1.57, 0))

def changeYaw(angle,vehicle):
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component,
                                    mavutil.mavlink.MAV_CMD_CONDITION_YAW, 0, angle, 25, 1, 0, 0, 0, 0)

def changeSpeed(speed,vehicle):
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component,
                                     mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0, 0, speed, 0, 0, 0, 0, 0)

# "LAND" "RTL" "GUIDED"
#vehicle.set_mode("GUIDED")

# bu komut da olabilir ? GPS_INPUT ( #232 )
#GPS_RTCM_DATA  233
def changeLocation():
    vehicle.mav.gps_input_send(
        0,  # Timestamp (micros since boot or Unix epoch)
        0,  # ID of the GPS for multiple GPS inputs
        # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
        # All other fields must be provided.
        (mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_HORIZ |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_VERT |
         mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY),
        0,  # GPS time (milliseconds from start of GPS week)
        0,  # GPS week number
        3,  # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
        0,  # Latitude (WGS84), in degrees * 1E7
        0,  # Longitude (WGS84), in degrees * 1E7
        0,  # Altitude (AMSL, not WGS84), in m (positive for up)
        1,  # GPS HDOP horizontal dilution of position in m
        1,  # GPS VDOP vertical dilution of position in m
        0,  # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in EAST direction in earth-fixed NED frame
        0,  # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
        0,  # GPS speed accuracy in m/s
        0,  # GPS horizontal accuracy in m
        0,  # GPS vertical accuracy in m
        7   # Number of satellites visible.
    )