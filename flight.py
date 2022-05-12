from cv2 import threshold
from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd
import math

def move_to_height(tello,height):
    cur_height = tello.get_state_field('z')
    to_move = abs(height - cur_height)
    to_move = 0 if to_move <= 10 else max(20,to_move)

    if to_move >= 20:
        if height - cur_height < 0:
            tello.move("down",to_move)
        else:
            tello.move("up",to_move)

def adjust_axis(axis, tello):
    # check by how much the drone has to move
    if axis == 'x':
        diff = 21 - tello.get_state_field(axis)
    else:
        diff = 0 - tello.get_state_field(axis)
    if abs(diff) <= 10:
        to_move = 0
    elif abs(diff) <= 20:
        to_move = 20
    else:
        to_move = abs(diff)

    # tello drone can only move at least 20 cm, so if we dont have to move it by that much we will not
    if to_move >= 20:
        if diff > 0:        
            if axis == 'x':
                tello.move("forward",to_move)
            elif axis == 'y':
                tello.move("left",to_move)
        elif diff < 0:        
            if axis == 'x':
                tello.move("back",to_move)
            elif axis == 'y':
                tello.move("right",to_move)

def micro_adjustments(tello):
    adjust_axis('x',tello)
    adjust_axis('y',tello)

# defining flights parameter
# Column, Front, Echelon, Vee,Diamond.
formation = "front"
movement = "hover"
wind_speed = 0
## speed 1: 5.4, speed 3: 8, speed 5: 12.5

wind_direction = "head_wind"
if wind_speed == 0:
    wind_direction = "none"

dist = 300
hover_time = 10

# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.111","192.168.0.112","192.168.0.113","192.168.0.114","192.168.0.115"]
start = [1,2,3,4,1]
dest = [5,6,7,8,5]
swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.enable_mission_pads())
swarm.parallel(lambda i,tello: tello.takeoff())
swarm.parallel(lambda i,tello: tello.set_mission_pad_detection_direction(2))

# fly
swarm.parallel(lambda i,tello: tello.set_speed(20))
swarm.parallel(lambda i,tello: tello.go_xyz_speed_mid(21,0,70,20,start[i]))
swarm.parallel(lambda i,tello: tello.move("forward",dist))
swarm.parallel(lambda i,tello: tello.go_xyz_speed_mid(21,0,70,20,dest[i]))
swarm.parallel(lambda i,tello: micro_adjustments(tello))

## hover
# swarm.parallel(lambda i,tello: tello.go_xyz_speed_mid(21,0,70,20,dest[i]))
# time.sleep(hover_time)

# end of flight
swarm.parallel(lambda i,tello: tello.land())
swarm.parallel(lambda i,tello: tello.disable_mission_pads())
swarm.parallel(lambda i, tello: tello.end())

# post flight
# retrieve log data
d=tello.STATE_LOG
data = pd.DataFrame(d)

import os
# write log data into files 1 file for each drone
# path: dataset/formation/movement/windspeed/winddirection
parent_folder = os.path.join("dataset",formation,movement,f"wind_speed_{wind_speed}",wind_direction)
# write data into csv
for ip in ips:
    to_write = data[data.address == ip]
    to_write.to_csv(f"{parent_folder}/drone{ip[-1]}.csv")

print(parent_folder)

