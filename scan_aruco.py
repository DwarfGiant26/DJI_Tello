import cv2
import droneblocksutils.aruco_utils
import math
from droneblocksutils.aruco_utils import detect_markers_in_image
import time
from djitellopy import Tello,TelloSwarm,tello

def default_velocity(instructions,time_lapsed):
    instruction = instructions[0] 
    start_coord = instruction[0]
    end_coord = instruction[1]
    time_to_complete = instruction[2]

    x_velocity = (end_coord[0] - start_coord[0])/time_to_complete
    y_velocity = (end_coord[0] - start_coord[0])/time_to_complete

    return (x_velocity,y_velocity)

def adjust(drone,default_speed,expected_coor,global_coor,frame_duration):
    # goal: try to adjust within 1 frame
    to_adjust_left_right = expected_coor[0] - global_coor[0]
    to_adjust_forward_backward = expected_coor[1] - global_coor[1]
    additional_x_speed = to_adjust_forward_backward / frame_duration
    additional_y_speed = to_adjust_left_right / frame_duration

    # make sure it is not going beyond the limit
    new_left_right_speed = max(min(default_speed[0] + additional_y_speed,100),-100)
    new_forward_backward_speed = max(min(default_speed[1] + additional_x_speed,100),-100)

    drone.send_rc_control(left_right_velocity = new_left_right_speed, \
        forward_backward_velocity = new_forward_backward_speed, \
        up_down_velocity = 0, \
        yaw_velocity = 0)

def pixel_to_cm(rel_coor_pixel):
    # start position: (112, 119)
    x_dis = abs(rel_coor_pixel[0] - 112) * 5 / 17
    y_dis = abs(rel_coor_pixel[1] - 119) * 5 / 17

    return (x_dis,y_dis)

def get_expected_completion_time(instructions,speed):
    start_coord = instructions[0]
    end_coord = instructions[1]
    dist = math.sqrt(((start_coord[0] - end_coord[0])**2) + ((start_coord[1] - end_coord[1])**2))
    # Seconds to complete the entire distance:
    time_to_complete = dist/speed
    return time_to_complete



def check_if_path_complete(current_coordinates, instructions, current_time):
    start_coord = instructions[0]
    end_coord = instructions[1]
    time_to_complete = instructions[2]
    # If drone is hovering:
    if(start_coord[0] == end_coord[0] and start_coord[1] == end_coord[1]):
        if current_time >= time_to_complete:
            return True
    # Else drone is moving to a destination, check if the drones current location is near the desired destination.
    else:
        if (current_coordinates[0] >= end_coord[0]-3 and current_coordinates[0] <= end_coord[0]+3):
            if (current_coordinates[1] >= end_coord[1] - 3 and current_coordinates[1] <= end_coord[1]+3):
                return True
    return False  
    # instructions[droneid]. Format : [(start,destination,time_to_complete), ...]     
    
def get_expected_coor(instructions,time_lapsed):
    #Intakes current coordinates,speed, time elapsed, and start and end coordinates. Returns expected coordinates. 
    # instructions=[(start x, start y), (endx, endy]
    # will need to adjust function depending on how time is tracked.

    instruction = instructions[0] 
    start_coord = instruction[0]
    end_coord = instruction[1]
    time_to_complete = instruction[2]
    instruction_start_time = 0 # change later so that it works with other instructions

    portion_complete = (time_lapsed-instruction_start_time)/time_to_complete

    x_expected = portion_complete*end_coord[0] + (1-portion_complete)*start_coord[0]
    y_expected = portion_complete*end_coord[1] + (1-portion_complete)*start_coord[1]
    expected_coord = (x_expected, y_expected)
    return expected_coord

def get_rel_pos(center_from_drone):
    DRONE_CENTER_COOR = (112,119)
    rel_coor = (center_from_drone[0]-DRONE_CENTER_COOR[0], center_from_drone[1]-DRONE_CENTER_COOR[1])
    
    return rel_coor 

def get_marker_coordinate(id):
    dist_x = 40
    dist_y = 40
    row_len_in_markers = 8
    id_start_0 = id - 85
    num_markers_from_0_x = id_start_0 % row_len_in_markers
    num_markers_from_0_y = id_start_0 // row_len_in_markers

    return(dist_x*num_markers_from_0_x, dist_y*num_markers_from_0_y)

def is_reaching_destination(cur_coor):
    pass

def expected_completion_time(instructions,velocity):
    pass

def move_precisely(drone,instructions):
    FRAME_DURATION = 0.2
    start_time = time.perf_counter()
    
    while True:
        cur_time = time.perf_counter()
        time_lapsed = cur_time - start_time

        # get image
        frame = drone.get_frame_read().frame

        # scan aruco from image
        image, arr = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True)
        if not len(arr) == 0:
            center_from_drone_pixel, id = arr[0]
        print(center_from_drone_pixel,id)
        # translate relative position to relative position using standard measurement
        center_from_drone_cm = pixel_to_cm(center_from_drone_pixel)
        rel_coor_cm = get_rel_pos(center_from_drone_cm)
        
        # translate relative position to global position
        curr_global_coordinate = rel_coor_cm + get_marker_coordinate(id)
        default_speed = default_velocity(instructions,time_lapsed)
        expected_coordinate = get_expected_coor(instructions,time_lapsed)
        
        # adjust based on the position and orientation
        adjust(drone,default_speed,expected_coordinate,curr_global_coordinate,FRAME_DURATION)

        if check_if_path_complete(curr_global_coordinate, instructions):
            break
        time.sleep(FRAME_DURATION)


if __name__ == "__main__":
    ips = ["192.168.0.113"]

    swarm = TelloSwarm.fromIps(ips)

    #beginning of flight
    swarm.parallel(lambda i,tello: tello.connect())
    swarm.parallel(lambda i,tello: tello.streamon())
    swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))

    instructions = [[((0,0),(140,0),5),]] # instructions[droneid]. Format : [(start,destination,time_to_complete), ...]
    swarm.parallel(lambda i,tello: tello.takeoff())
    move_precisely(swarm.tellos[0],instructions[0],velocity=(20,0))
    swarm.parallel(lambda i,tello: move_precisely(tello,instructions[i],))

    swarm.parallel(lambda i,tello: tello.streamoff())

    # end of flight
    swarm.parallel(lambda i,tello: tello.land())
    swarm.parallel(lambda i, tello: tello.end())
