from cv2 import threshold
from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd
import math

# defining flights parameter
# Column, Front, Echelon, Vee,Diamond.
formation = "front"
movement = "forward"
wind_speed = 1
wind_direction = "head_wind"
if wind_speed == 0:
    wind_direction = "none"
dist = 200
hover_time = 5

# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.111","192.168.0.112","192.168.0.113","192.168.0.114","192.168.0.115"]
start = [1,2,3,4,1]
dest = [5,6,7,8,5]
swarm = TelloSwarm.fromIps(ips)

#pre flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.enable_mission_pads())
swarm.parallel(lambda i,tello: tello.takeoff())
swarm.parallel(lambda i,tello: tello.set_mission_pad_detection_direction(2))


# fly
swarm.parallel(lambda i,tello: tello.move("forward",dist))
swarm.parallel(lambda i,tello: tello.go_xyz_speed_mid(0,0,70,100,dest[i]))

swarm.parallel(lambda i,tello: tello.land())
swarm.parallel(lambda i,tello: tello.disable_mission_pads())

# Tell all drones in swarm to end their instance
swarm.parallel(lambda i, tello: tello.end())

# store the log data
d=tello.STATE_LOG
data = pd.DataFrame(d)

import os

# path: dataset/formation/movement/windspeed/winddirection
parent_folder = os.path.join("dataset",formation,movement,f"wind_speed_{wind_speed}",wind_direction)
# write data into csv
for ip in ips:
    to_write = data[data.address == ip]
    to_write.to_csv(f"{parent_folder}/drone{ip[-1]}.csv")


# def micro_adjustments(tello):
#     # inacuraccy threshold
#     threshold = 2
#     while(math.abs(tello.get_state_field('x'))> threshold and math.abs(tello.get_state_field('y')) > threshold):
#         if tello.get_state_field('x') > 0:
#             tello.move("back",math.abs())