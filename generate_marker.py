import cv2

dictionary = cv2.aruco.cv2.aruco.DICT_4X4_1000

for i in range(81):
    cv2.aruco.drawMarker(dictionary,i,250,)