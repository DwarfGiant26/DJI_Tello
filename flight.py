from cv2 import threshold
from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd
import math
from adjustment import move_precisely

# defining flights parameter
# Column, Front, Echelon, Vee,Diamond.
# column : 70cm between drone, 1 is the southest 5 is the northest

formation = "column"
movement = "hover"
wind_speed = 0
## speed 1: 5.4, speed 3: 8, speed 5: 12.5

wind_direction = "tail_wind"
if wind_speed == 0:
    wind_direction = "none"

dist = 100
hover_time = 60

# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.111","192.168.0.112","192.168.0.113","192.168.0.114","192.168.0.115"]
ips = ["192.168.0.103"]
swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.set_vs_port(f"1200{i-1}"))
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
time.sleep(5)

# instructions[droneid]. Format : [(start,destination,time_to_complete), ...]
instructions = [[((40,160),(40,160),20)],[((110,160),(110,160),120)],[((180,160),(180,160),120)],[((250,160),(250,160),120)],[((320,160),(320,160),120)],] 
swarm.parallel(lambda i,tello: tello.takeoff())
swarm.parallel(lambda i,tello: move_precisely(tello,instructions[i]))

swarm.parallel(lambda i,tello: tello.streamoff())

# end of flight
swarm.parallel(lambda i,tello: tello.land())
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

