from requests import get
from djitellopy import Tello,TelloSwarm,tello
import cv2
from droneblocksutils.aruco_utils import detect_markers_in_image

# from cv2 import aruco
# ip: 192.168.0.11<drone number>
# defining the drones
ips = ["192.168.0.113"]

swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
cap = swarm.tellos[0].get_frame_read()
import time

while True:
  cap = swarm.tellos[0].get_frame_read()
  cv2.imshow('Frame', cap.frame)
  if cv2.waitKey(25) & 0xFF == ord('q'):
    break
  swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
  image, arr = detect_markers_in_image(cap.frame, draw_center=True, draw_reference_corner=True)
  if not len(arr) == 0:
    center, id = arr[0]
    print(id)
    print(center)
  
  time.sleep(0.5)


swarm.parallel(lambda i,tello: tello.streamoff())

# post flight
# retrieve log data
# d=tello.STATE_LOG
# data = pd.DataFrame(d)

# import os
# # write log data into files 1 file for each drone
# # path: dataset/formation/movement/windspeed/winddirection
# parent_folder = os.path.join("dataset",formation,movement,f"wind_speed_{wind_speed}",wind_direction)
# # write data into csv
# for ip in ips:
#     to_write = data[data.address == ip]
#     to_write.to_csv(f"{parent_folder}/drone{ip[-1]}.csv")
#
# print(parent_folder)

