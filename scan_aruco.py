import cv2
import Math
import droneblocksutils.aruco_utils
from droneblocksutils.aruco_utils import detect_markers_in_image

# extern aruco_dict

# global aruco_dict = cv2.aruco.dictionary_get(cv2.aruco.DICT_4x4_1000)

def adjust(drone,expected_coor, global_coor):
    pass


def pixel_to_cm(rel_coor_pixel):
    pass

def get_expected_coor(instructions,time,curr_coordinates,speed):
    #Intakes current coordinates,speed, time elapsed, and which direction it should intake. Returns expected coordinates. 
    # instructions=[(start x, start y), (endx, endy)]
    start_coord = instructions[0]
    end_coord = instructions[1]
    dist = Math.sqrt(((start_coord[0] - end_coord[0])**2) + ((start_coord[1] - end_coord[1])**2))
    # Seconds to complete the entire distance:
    time_to_complete = dist/speed
    # What percentage of the journey should have been completed so far:
    time_elapsed = time/time_to_complete
    # Total distance which should be travelled in the x plane so far:
    x_travelled = time_elapsed*(abs(start_coord[0] - end_coord[0])) 
    # Total distance which should be travelled in the y plane so far:
    y_travelled = time_elapsed*(abs(start_coord[1] - end_coord[1]))
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








def move_precisely(drone,flight_path,instructions):

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
    # adjust based on the position and orientation
    adjust(drone,expected_coordinate,curr_global_coordinate)

def get_marker_coordinate(id):
    dist_x = 30
    dist_y = 30
    row_len_in_markers = 3
    num_markers_from_0_x = id % row_len_in_markers
    num_markers_from_0_y = id // row_len_in_markers

    return(dist_x*num_markers_from_0_x, dist_y*num_markers_from_0_y)

