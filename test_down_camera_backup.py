from requests import get
from djitellopy import Tello,TelloSwarm,tello
import cv2
from droneblocksutils.aruco_utils import detect_markers_in_image

# from cv2 import aruco
# ip: 192.168.0.11<drone number>
# defining the drones
ips = [f"192.168.0.11{i}" for i in range(1,6)]
swarm = TelloSwarm.fromIps(ips)

swarm.parallel(lambda i,tello: tello.set_vs_port(f"1400{i+1}"))
#beginning of flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
cap = [swarm.tellos[i].get_frame_read() for i in range(5)]

while True:
  for i in range(0,5):
    cv2.imshow(f'Drone{i+1}', cap[i].frame)

  if cv2.waitKey(25) & 0xFF == ord('q'):
    break
  # swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))
  # image, arr = detect_markers_in_image(cap.frame, draw_center=True, draw_reference_corner=True)
  # if not len(arr) == 0:
  #   center, id = arr[0]
  #   print(id)
  #   print(center)
  
  # time.sleep(0.5)


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

