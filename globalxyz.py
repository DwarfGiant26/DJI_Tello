# convert xyz based on different mission pad to xyz based on a single mission pad
import pandas as pd

csv_path = "dataset/front/forward/wind_speed_0/none/drone1.csv"
df = pd.read_csv(csv_path)

""" front
forward
1, start(0,0), end(200,0) 1,5
2, start(0,50), end(200,50) 2,6
3, start(0,100), end(200,100) 3,7
4, start(0,150), end(200,150) 4,8
5, start(0,200), end(200,200) 1,5

hovering
everything is the same except it does not have end node
"""

# key: <drone number,mid>

pad_coor = {}

# front
pad_coor['1,1'] = (0,200)
pad_coor['1,5'] = (200,200)
pad_coor['2,2'] = (0,150)
pad_coor['2,6'] = (200,150)
pad_coor['3,3'] = (0,100)
pad_coor['3,7'] = (200,100)
pad_coor['4,4'] = (0,50)
pad_coor['4,8'] = (200,50)
pad_coor['5,1'] = (0,0)
pad_coor['5,5'] = (200,0)

for i,rows in enumerate(df):
    pad_id = rows['mid']
    rel_x = rows['x']
    rel_y = rows['y']
    drone_number = rows['ip']
    pad_coordinate = pad_coor[f"{drone_number},{pad_id}"]
    global_x = pad_coordinate[0] + rel_x
    global_y = pad_coordinate[1] + rel_y
    df['global_x'][i] = global_x
    df['global_y'][i] = global_y

df.to_csv()