from cv2 import threshold
from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd
import math

# defining the drones
pad_id = 2
t = Tello("192.168.0.111")

#beginning of flight
t.connect()
t.enable_mission_pads()
t.takeoff()
t.set_mission_pad_detection_direction(2)

# fly
while True:
    try:
        t.go_xyz_speed_mid(21,0,70,20,pad_id)
        # retrieve log data
        time.sleep(10)
    except:
        break

d=tello.STATE_LOG
data = pd.DataFrame(d)
data.to_csv('hovering_battery_consumption.csv')