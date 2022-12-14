import asyncio
import logging
from sys import argv

from growatt_client import GrowattClient

# defaults
# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)


async def main():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    client = GrowattClient(port, address)
    try:
        data = await client.async_update()
        print(f"Sensors data: {data}")
    except Exception as error:
        print(error)
        print("Error: " + repr(error))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
