from collections import defaultdict
import json
import logging
import sys
import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# All CO2 readings
co2_per_car = defaultdict(list)
def lambda_handler(event, context):
    global co2_per_car

    # Only process data that comes from a vehicle with co2 data.
    if ("vehicle" not in event or "co2" not in event):
        return

    # Get your data
    vehicle_id = event["vehicle"]
    co2 = event["co2"]

    # Cache it in the global data.
    co2_per_car[vehicle_id].append(co2)

    # Calculate max CO2 emission
    max_co2_for_vehicle = max(co2_per_car[vehicle_id])

    # Return the result
    topic = "co2/" + vehicle_id
    message = "Max CO2 for car {}: {}".format(vehicle_id, max_co2_for_vehicle)
    logging.debug(topic + ' <--- ' + message)
    client.publish(
        topic=topic,
        payload=json.dumps({"message": message}),
    )

    return

# For debugging locally without greengrass:
# lambda_handler({"vehicle" : "V01", "co2" : 3}, '')
# lambda_handler({"vehicle" : "V02", "co2" : 4}, '')
# lambda_handler({"vehicle" : "V01", "co2" : 1}, '')
# lambda_handler({"vehicle" : "V02", "co2" : 2}, '')
# lambda_handler({"vehicle" : "V01", "co2" : 5}, '')
# lambda_handler({"vehicle" : "V02", "co2" : 6}, '')