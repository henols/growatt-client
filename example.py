import asyncio
import logging
from sys import argv

from growatt_client import GrowattClient

# defaults
# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x00

logging.basicConfig(level=logging.INFO)


async def main():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    client = GrowattClient(port, address)
    try:
        ser = client.get_serial_number()
        logging.info(
            f" Serial number: {ser} "
            f"Firmware: {client.get_firmware()} "
            f"Model Number: {client.get_model_number()}"
        )

        data = await client.async_update()

        logging.debug(f"Sensors data: {data}")
        for key in data:
            desc = client.get_attribute(key)
            value = data[key]
            d = desc["description"]
            u = desc["unit"]
            logging.info(f"{d} {value} {u}")

    except Exception as error:
        logging.error("Error: " + repr(error))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
