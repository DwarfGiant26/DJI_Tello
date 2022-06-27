import cv2
import droneblocksutils.aruco_utils
import math
from droneblocksutils.aruco_utils import detect_markers_in_image


from scan_aruco import get_expected_coor
from scan_aruco import get_expected_completion_time
from scan_aruco import check_if_path_complete


instructions = [(1,0),(0, 350),45]
instructions1 = [(1,0),(1, 0),25]
time=2
speed=13
# expected_coords = get_expected_coor(instructions, time, speed)
# print(expected_coords)

# expected_time = get_expected_completion_time(instructions,speed)
# print(expected_time)



# def check_if_path_complete(current_coordinates, instructions, current_time):

is_complete = check_if_path_complete((4,350),instructions,20)
is_complete1 = check_if_path_complete((3,0),instructions1,25)
print(is_complete1)

