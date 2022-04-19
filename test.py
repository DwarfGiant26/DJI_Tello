from djitellopy import Tello,TelloSwarm,tello
import time
import pandas as pd

ips = ["192.168.0.101","192.168.0.103"]
t = TelloSwarm.fromIps(ips)
t.parallel(lambda i,tello: tello.connect())
t.parallel(lambda i,tello: tello.takeoff())
t.parallel(lambda i,tello: tello.enable_mission_pads())
t.parallel(lambda i,tello: tello.set_mission_pad_detection_direction(2))
t.parallel(lambda i,tello: tello.move("forward",100))
t.parallel(lambda i,tello: tello.move("back",100))
time.sleep(2)
t.parallel(lambda i,tello: tello.land())
t.parallel(lambda i,tello: tello.disable_mission_pads())

#Tell all drones in swarm to end their instance
t.parallel(lambda i, tello: tello.end())
d=tello.STATE_LOG
data = pd.DataFrame(d)
#drop mid if we are not using the pads
#data = data.drop(columns=['mid'])


#write data into csv
for ip in ips:
    to_write = data[data.address == ip]
    to_write.to_csv(f"test_log{ip}.csv")