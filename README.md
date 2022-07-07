## Project description
This repository contains the code to fly a swarm of DJI tello edu drones and collect their state data. 

## File descriptions

Folder **djitellopy** comes from the original DJI Tello drone python interface from https://github.com/damiafuentes/DJITelloPy. swarm.py and enforces_types.py are unmodified, whereas tello.py had some modification to easily access state data for individual or swarm of tellos.

* swarm.py is the original file and allows to create and give command to a swarm created using ip addresses from a txt file.
* enforce_types.py is the original file
* tello.py was modified by adding a global STATE.LOG which records the state data from each connected drone. Additional modification were made so that each observation has a timestamp and the ip address from the drone.

*data_collection.iypnb is a notebook with the necessary code to initialize a swarm, make the swarm take off, hover for 30 sec, extract the data and export it to a csv file.
## Instructions

### How to fly a swarm and collect data for 30 seconds

**IMPORTANT** : a router is necessary to be able to fly a swarm. 

To create a swarm. The first step is to reconfigure each drone of the swarm individually and set them to station mode.

To do so we use the software packet sender and do the following for each drone of the swarm:

1. Connect to the tello's wifi
2. Put the tello into SDK mode by sending the command: command 
3. Then send the command: ap router_wifi_name password_of_the_router       (i.e: ap WIFI_E949 87094848)

#### To fly the drone using aruco marker

1. Place drone facing north in the map.
2. import ajdustment
3. specify the instructions with format instructions = [drone1_instructions, drone2_instructions, drone3_instructions, drone4_instructions, ...]
The format of dronex_instructions = [instruction1, instruction2, ...]
The format of each instruction = ((start_x,start_y,start_z),(dest_x,dest_y,dest_z),time_to_complete)
The example can be found in flight.py
4. run ./udp_forward
5. set vs port for each drone, and down vision. Example in flight.py
6. fly the drone using move_precisely(). Example in flight.py
