import asyncio
import logging
from sys import argv

from growatt_client import GrowattClient

# defaults
# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x01

logging.basicConfig(level=logging.INFO)


async def run_async_client():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    client = GrowattClient(port, address)

    data = await client.async_update()
    ser = client.get_serial_number()

    logging.info(
        f" Serial number: {ser} "
        f"Firmware: {client.get_firmware()} "
        f"Model Number: {client.get_model_number()}"
    )

    logging.debug(f"Sensors data: {data}")
    for key in sorted(data):
        desc = client.get_attribute(key)
        value = data[key]
        d = desc["description"]
        u = desc["unit"]
        calculated = "(calculated)" if "template" in desc else ""
        logging.info(f"{d} {value} {u} {calculated}")

    # except Exception as error:
    #     logging.error("Error: " + repr(error))


if __name__ == "__main__":
    asyncio.run(run_async_client())
