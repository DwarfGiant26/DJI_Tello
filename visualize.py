import pandas as pd

csv_path = "dataset/front/forward/wind_speed_1/head_wind/drone1.csv"
df = pd.read_csv(csv_path)


print(df)