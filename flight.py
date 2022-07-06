from cv2 import threshold
from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd
import math
from adjustment import move_precisely,set_background_frame
import os

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

hover_time = 15

# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.111","192.168.0.112","192.168.0.113","192.168.0.114","192.168.0.115"]
swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.set_vs_port(f"1400{i+1}"))
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: set_background_frame(tello))
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
time.sleep(5)

# instructions[droneid]. Format : [(start,destination,time_to_complete), ...]
# instructions = [[((40,160,80),(40,160,80),hover_time)],[((110,160),(110,160),hover_time)],[((180,160),(180,160),hover_time)],[((250,160),(250,160),hover_time)],[((320,160),(320,160),hover_time)],] 
instructions = [[((40,160,80),(40,160,80),hover_time),((40,160,80),(40,160,100),100)]]

swarm.parallel(lambda i,tello: tello.takeoff())
swarm.parallel(lambda i,tello: move_precisely(tello,instructions[i],open(os.path.join("MovePreciselyLog",f"drone{i+1}"),"w")))

swarm.parallel(lambda i,tello: tello.streamoff())

# end of flight
swarm.parallel(lambda i,tello: tello.land())
swarm.parallel(lambda i, tello: tello.end())

# post flight
# retrieve log data
d=tello.STATE_LOG
data = pd.DataFrame(d)

# write log data into files 1 file for each drone
# path: dataset/formation/movement/windspeed/winddirection
parent_folder = os.path.join("dataset",formation,movement,f"wind_speed_{wind_speed}",wind_direction)
# write data into csv
for ip in ips:
    to_write = data[data.address == ip]
    to_write.to_csv(f"{parent_folder}/drone{ip[-1]}.csv")

print(parent_folder)

