import os

# path: dataset/formation/movement/windspeed/winddirection
os.mkdir('dataset')
os.chdir('dataset')
for i in ['column', 'front', 'echelon', 'vee', 'diamond']:
    os.mkdir(i)
    for j in ['forward','hover']:
        os.mkdir(os.path.join(i,j))
        for k in [0,1,3,5]:
            os.mkdir(os.path.join(i,j,f'wind_speed_{k}'))
            dirs = ["none"] if k == 0 else ["head_wind","tail_wind","cross_wind"]   
            for l in dirs:
                os.mkdir(os.path.join(i,j,f'wind_speed_{k}',l))
