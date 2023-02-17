# GrowattClient

[![PyPI][pypi-releases-shield]][pypi-releases]
[![GitHub issues](https://img.shields.io/github/issues/henols/growatt-client.svg)](https://github.com/henols/growatt-client/issues/)

Python wrapper for getting data asynchronously from Growatt inverters via serial usb RS232 connection and modbus RTU protocol.

The Growatt inverted must support the modbus protocol (some older inverters only support proprietary serial communication)
Connect the RS232 DB9 usb adapter to the RS232 port on the underside of the inverter (you might have to remove a cover plate).

## Attributes

Depending on the firmware version of your inverter, not all attributes might be available

Inverter properties

- serial_number
- model_number
- firmware

[Supprted attributes](attributes.md)

## How to use the package

```py
import asyncio
import logging
from sys import argv

from growatt-client.growatt import GrowattClient

# defaults
# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)


async def main():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    growatt_client = GrowattClient(port, address)
    try:
        data = await growatt_client.async_update()
        print(f"Sensors data: {data}")
    except Exception as error:
        print("Error: " + repr(error))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

[pypi-releases]: https://pypi.org/project/growatt-client
[pypi-releases-shield]: https://img.shields.io/pypi/v/growatt-client
