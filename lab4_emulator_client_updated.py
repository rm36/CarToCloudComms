# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#Starting and end index
device_st = 1
device_end = 6

#Path to the dataset, modify this
data_path = "vehicle/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./certs/my_thing_{id:03d}_cert.pem"
key_formatter = "./certs/my_thing_{id:03d}_private.key"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        # The broker address
        self.client.configureEndpoint("adz916uy5o53j-ats.iot.us-east-1.amazonaws.com", 8883)
        self.client.configureCredentials("./certificates_amazon/AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        print("Vehicle {} received {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        pass


    def publish(self, topic, payload):
        print("Reporting data to " + topic + ": " + payload)
        self.client.publishAsync(topic, payload, 0, ackCallback=self.customPubackCallback)

    def subscribe(self, topic):
        self.client.subscribeAsync(topic, 0, ackCallback=self.customSubackCallback)


print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id, certificate_formatter.format(id=device_id), key_formatter.format(id=device_id))
    client.client.connect()
    clients.append(client)
 
current_timestep = 0

for i,c in enumerate(clients):
    c.subscribe("co2/v{id:03d}".format(id=i+1))

while True:
    print("Press Enter to simulate sending CO2 data from each vehicle...")
    x = input()

    for i,c in enumerate(clients):
        co2 = data[i]['vehicle_CO2'][current_timestep]
        noise = data[i]['vehicle_noise'][current_timestep]
        x = data[i]['vehicle_x'][current_timestep]
        y = data[i]['vehicle_y'][current_timestep]
        message = {"vehicle" : "v{id:03d}".format(id=i+1), "co2":co2, "noise":noise, "x":x, "y":y}
        c.publish(topic = "co2/report", payload=json.dumps(message))
    current_timestep += 1

    time.sleep(1)