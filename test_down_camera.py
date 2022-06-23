from requests import get
from djitellopy import Tello,TelloSwarm,tello
import cv2
from cv2 import aruco
# ip: 192.168.0.11<drone number> 
# defining the drones
ips = ["192.168.0.111"]

swarm = TelloSwarm.fromIps(ips)

#beginning of flight
swarm.parallel(lambda i,tello: tello.connect())
swarm.parallel(lambda i,tello: tello.streamon())
swarm.parallel(lambda i,tello: tello.send_control_command("downvision 0"))
print(swarm.tellos)
cap = swarm.tellos[0].get_video_capture()

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Display the resulting frame
    cv2.imshow('Frame',frame)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

swarm.parallel(lambda i,tello: tello.streamoff())

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

