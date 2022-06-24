import cv2
import droneblocksutils.aruco_utils
from droneblocksutils.aruco_utils import detect_markers_in_image
import time
from djitellopy import Tello,TelloSwarm,tello

# extern aruco_dict

# global aruco_dict = cv2.aruco.dictionary_get(cv2.aruco.DICT_4x4_1000)

def adjust(drone,expected_coor, global_coor):
    pass

def pixel_to_cm(rel_coor_pixel):
    pass

def get_expected_coor(instructions,time):
    pass

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
        rel_coor_cm = pixel_to_cm(rel_coor_pixel)
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
