from xml.dom.expatbuilder import parseFragmentString
import cv2
import Math
import droneblocksutils.aruco_utils
from droneblocksutils.aruco_utils import detect_markers_in_image
import time
from djitellopy import Tello,TelloSwarm,tello

def default_velocity(instructions,time_lapsed):
    pass


def adjust(drone,velocity,expected_coor, global_coor,frame_duration):
    to_adjust_left_right = expected_coor[0] - global_coor[0]
    to_adjust_forward_backward = expected_coor[1] - global_coor[1]
    additional_x_speed = to_adjust_forward_backward / frame_duration
    additional_y_speed = to_adjust_left_right / frame_duration

    drone.send_rc_control(left_right_velocity = , \
        forward_backward_velocity = 0, \
        up_down_velocity = 0, \
        yaw_velocity = 0)
    pass

def pixel_to_cm(rel_coor_pixel):
    pass

def get_expected_completion_time(instructions,time,speed):
    start_coord = instructions[0]
    end_coord = instructions[1]
    dist = Math.sqrt(((start_coord[0] - end_coord[0])**2) + ((start_coord[1] - end_coord[1])**2))
    # Seconds to complete the entire distance:
    time_to_complete = dist/speed
    return time_to_complete


def get_expected_coor(instructions,time,speed):
    #Intakes current coordinates,speed, time elapsed, and start and end coordinates. Returns expected coordinates. 
    # instructions=[(start x, start y), (endx, endy]
    # will need to adjust function depending on how time is tracked. 
    start_coord = instructions[0]
    end_coord = instructions[1]
    dist = Math.sqrt(((start_coord[0] - end_coord[0])**2) + ((start_coord[1] - end_coord[1])**2))
    # Seconds to complete the entire distance:
    time_to_complete = dist/speed
    # What percentage of the journey should have been completed so far:
    portion_complete = time/time_to_complete
    # Total distance which should be travelled in the x plane so far:
    x_travelled = portion_complete*(abs(start_coord[0] - end_coord[0])) 
    # Total distance which should be travelled in the y plane so far:
    y_travelled = portion_complete*(abs(start_coord[1] - end_coord[1]))
    # If the drone needs to travel in increasing x coordinate values:
    if(start_coord[0] < end_coord[0]):
        x_expected = start_coord[0] + x_travelled
    # Drone travels in decreasing y coordinate values. 
    else:
        x_expected = start_coord[0] - x_travelled

    # If the drone needs to travel in increasing y coordinate values:
    if(start_coord[1] < end_coord[1]):
        y_expected = start_coord[1] + y_travelled
    # Drone travels in decreasing y coordinate values.
    else:
        y_expected = start_coord[1] - y_travelled
    expected_coord = (x_expected, y_expected)
    return expected_coord

def get_rel_pos(center_from_drone):
    parseFragmentString

def get_marker_coordinate(id):
    dist_x = 30
    dist_y = 30
    row_len_in_markers = 3
    num_markers_from_0_x = id % row_len_in_markers
    num_markers_from_0_y = id // row_len_in_markers

    return(dist_x*num_markers_from_0_x, dist_y*num_markers_from_0_y)

def is_reaching_destination(cur_coor):
    pass

def expected_completion_time(instructions,velocity):
    pass

def move_precisely(drone,instructions,velocity):
    start_time = time.perf_counter()
    expected_completion_time = expected_completion_time(instructions,velocity)
    
    while True:
        # todo: set an adjusts rate i.e. how many adjustments per seconds
        cur_time = time.perf_counter()
        # stop if the time is passed and we are reaching destination
        if cur_time - start_time > expected_completion_time:
            break

        # get image
        frame = drone.get_frame_read().frame
        # scan aruco from image
        image, arr = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True)
        if not len(arr) == 0:
            rel_coor_pixel, id = arr[0]

        # translate relative position to relative position using standard measurement
        center_from_drone = pixel_to_cm(rel_coor_pixel)
        rel_coor_cm = get_rel_pos(center_from_drone)
        
        # translate relative position to global position
        curr_global_coordinate = rel_coor_cm + get_marker_coordinate(id)
        expected_coordinate = get_expected_coor(instructions,time)
        # adjust based on the position and orientation
        adjust(drone,expected_coordinate,curr_global_coordinate)


if __name__ == "__main__":
    ips = ["192.168.0.111"]

    swarm = TelloSwarm.fromIps(ips)

    #beginning of flight
    swarm.parallel(lambda i,tello: tello.connect())
    swarm.parallel(lambda i,tello: tello.streamon())
    swarm.parallel(lambda i,tello: tello.send_control_command("downvision 1"))

    instructions = [[((0,0),(100,100)),]] # instructions[droneid]
    swarm.parallel(lambda i,tello: tello.takeoff())
    swarm.parallel(lambda i,tello: move_precisely(tello,instructions[i],velocity=20))
    swarm.parallel(lambda i,tello: tello.streamoff())

    # end of flight
    swarm.parallel(lambda i,tello: tello.land())
    swarm.parallel(lambda i, tello: tello.end())
