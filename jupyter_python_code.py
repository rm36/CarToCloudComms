import boto3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# create IoT Analytics client
client = boto3.client('iotanalytics')


dataset = "mydataset"
dataset_url = client.get_dataset_content(datasetName = dataset)['entries'][0]['dataURI']
data = pd.read_csv(dataset_url)

# Get CO2 data from dataset
v1_co2 = data[data["vehicle"]=="v001"]["co2"].to_numpy()
v2_co2 = data[data["vehicle"]=="v002"]["co2"].to_numpy()
v3_co2 = data[data["vehicle"]=="v003"]["co2"].to_numpy()
v4_co2 = data[data["vehicle"]=="v004"]["co2"].to_numpy()
v5_co2 = data[data["vehicle"]=="v005"]["co2"].to_numpy()

# plot lines
plt.plot(v1_co2, label = "Vehicle 1 CO_2")
plt.plot(v2_co2, label = "Vehicle 2 CO_2")
plt.plot(v3_co2, label = "Vehicle 3 CO_2")
plt.plot(v4_co2, label = "Vehicle 4 CO_2")
plt.plot(v5_co2, label = "Vehicle 5 CO_2")
plt.legend()
plt.show()



# Get CO2 data from dataset
v1_noise = data[data["vehicle"]=="v001"]["noise"].to_numpy()
v2_noise = data[data["vehicle"]=="v002"]["noise"].to_numpy()
v3_noise = data[data["vehicle"]=="v003"]["noise"].to_numpy()
v4_noise = data[data["vehicle"]=="v004"]["noise"].to_numpy()
v5_noise = data[data["vehicle"]=="v005"]["noise"].to_numpy()

# plot lines
plt.plot(v1_noise, label = "Vehicle 1 noise")
plt.plot(v2_noise, label = "Vehicle 2 noise")
plt.plot(v3_noise, label = "Vehicle 3 noise")
plt.plot(v4_noise, label = "Vehicle 4 noise")
plt.plot(v5_noise, label = "Vehicle 5 noise")
plt.legend()
plt.show()



# Get CO2 data from dataset
v1_x = data[data["vehicle"]=="v001"]["x"].to_numpy()
v2_x = data[data["vehicle"]=="v002"]["x"].to_numpy()
v3_x = data[data["vehicle"]=="v003"]["x"].to_numpy()
v4_x = data[data["vehicle"]=="v004"]["x"].to_numpy()
v5_x = data[data["vehicle"]=="v005"]["x"].to_numpy()
v1_y = data[data["vehicle"]=="v001"]["y"].to_numpy()
v2_y = data[data["vehicle"]=="v002"]["y"].to_numpy()
v3_y = data[data["vehicle"]=="v003"]["y"].to_numpy()
v4_y = data[data["vehicle"]=="v004"]["y"].to_numpy()
v5_y = data[data["vehicle"]=="v005"]["y"].to_numpy()

# plot lines
plt.plot(v1_x, v1_y, label = "Vehicle 1 trajectory")
plt.plot(v2_x, v2_y, label = "Vehicle 2 trajectory")
plt.plot(v3_x, v3_y, label = "Vehicle 3 trajectory")
plt.plot(v4_x, v4_y, label = "Vehicle 4 trajectory")
plt.plot(v5_x, v5_y, label = "Vehicle 5 trajectory")
plt.legend()
plt.show()