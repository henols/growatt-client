import time
import json
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import logging
import asyncio

from sys import argv

from growatt_client import GrowattClient

# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x00

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("Mqtt-example")

connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"connected OK to MQTT Returned code={rc}")
        global connected
        connected = True
    else:
        logger.warning(f"Bad connection Returned code={rc}")


port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
client = GrowattClient(port, address)

mqtt_client = mqtt.Client("inverter")
mqtt_client.on_connect = on_connect
mqtt_client.connect("aceone.se")
mqtt_client.loop_start()

while not connected:
    time.sleep(2)

payload = {"name": "Growatt MQTT", "unique_id": "growatt_inverter"}
logger.info(payload)
mqtt_client.publish(
    "homeassistant/sensor/growattmqtt/config",
    payload=json.dumps(payload),
    retain=True,
)

# NAMES = [
#     "pv1_wattage",
#     "pv1_energy_today",
#     "pv1_energy_lifetime",
#     "pv2_wattage",
#     "pv2_energy_today",
#     "pv2_energy_lifetime",
#     ]
# for name in NAMES:
#     mqtt_client.publish(
#         "homeassistant/sensor/growatt_" + name + "/config",
#         payload="",
#         # payload=json.dumps(payload),
#         retain=True,
#     )



for reg in client.get_attributes():
    name = reg["name"]
    unit = reg["unit"]
    desc = reg["description"]
    if unit == "kWh":
        class_type = "energy"
    elif unit == "kW":
        class_type = "power"
    elif unit == "v":
        class_type = "battery"
    elif unit == "v":
        class_type = "voltage"
    elif unit == "ts":
        class_type = "timestamp"

    unique_id = "growatt_inverter_" + name
    topic = "inverter/growattmqtt/" + name

    payload = {
        "device_class": class_type,
        "name": desc,
        "state_topic": topic,
        "unit_of_measurement": unit,
        "unique_id": unique_id,
        "device": {
            "identifiers": ["growatt_inverter"],
            "name": "growatt_inverter",
        },
    }

    logger.info(payload)

    mqtt_client.publish(
        "homeassistant/sensor/growatt_" + name + "/config",
        payload=json.dumps(payload),
        retain=True,
    )


async def main():
    try:
        while True:
            regs = await client.async_update()
            for key, value in regs.items():
                logger.info(f"name: {key}, value: {value}")
                mqtt_client.publish(
                    "inverter/growattmqtt/" + key, payload=value
                )
            time.sleep(30)
            logger.info("")
    except Exception as error:
        logger.error("Error: " + repr(error))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
