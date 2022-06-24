import cv2
import droneblocksutils.aruco_utils

# extern aruco_dict

# global aruco_dict = cv2.aruco.dictionary_get(cv2.aruco.DICT_4x4_1000)

def adjust(expected_coor, global_coor):
    pass

def get_info_aruco(frame):
    pass

def move_precisely(drone,flight_path,):

    # get image
    frame = drone.get_frame_read()
    # scan aruco from image
    id,position,orientation = get_info_aruco(frame)
    
    image, arr = detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True)

    # translate relative position to relative position using standard measurement
    # translate relative position to global position

    # adjust based on the position and orientation
    adjust(expected_coordinate,global_coordinate)

def get_marker_coordinate(id):
    dist_x = 30
    dist_y = 30
    row_len_in_markers = 3
    num_markers_from_0_x = id % row_len_in_markers
    num_markers_from_0_y = id // row_len_in_markers

    return(dist_x*num_markers_from_0_x, dist_y*num_markers_from_0_y)

