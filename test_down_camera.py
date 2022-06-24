from requests import get
from djitellopy import Tello,TelloSwarm,tello
# import cv2
# from droneblocksutils.aruco_utils import detect_markers_in_image
# from cv2 import aruco
# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.113"]

swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
print(swarm.tellos)
cap = swarm.tellos[0].get_frame_read()
while True:

  print(swarm.tellos[0].get_yaw())


swarm.parallel(lambda i,tello: tello.streamoff())


def pixel_to_cm(rel_coor_pixel):
  x_pixel_distance = rel_coor_pixel[1][0] - rel_coor_pixel[0][0]
  y_pixel_distance = rel_coor_pixel[1][1] - rel_coor_pixel[0][1]
  x_real_distance = (x_pixel_distance) * 5 / 17
  y_real_distance = (y_pixel_distance) * 5 / 17



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

