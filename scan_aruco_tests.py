import cv2
import droneblocksutils.aruco_utils
import math
from droneblocksutils.aruco_utils import detect_markers_in_image


from scan_aruco import get_expected_coor
from scan_aruco import get_expected_completion_time


instructions = [(1,0),(0, 350)]
time=4
speed=13
expected_coords = get_expected_coor(instructions, time, speed)
print(expected_coords)

expected_time = get_expected_completion_time(instructions,speed)
print(expected_time)