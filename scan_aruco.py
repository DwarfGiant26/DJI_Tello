def adjust(expected_coor, global_coor):
    pass

def get_info_aruco(frame):
    pass

def move_precisely(drone,flight_path,):
    # get image
    frame = drone.get_frame_read()
    # scan aruco from image
    id,position,orientation = get_info_aruco(frame)
    
    # detect_markers_in_image(frame, draw_center=True, draw_reference_corner=True)
    # translate relative position to relative position using standard measurement
    # translate relative position to global position

    # adjust based on the position and orientation
    adjust(expected_coordinate,global_coordinate)

def get_marker_coordinate(id):
    
