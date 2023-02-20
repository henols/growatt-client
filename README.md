# GrowattClient

[![PyPI][pypi-releases-shield]][pypi-releases]
[![GitHub issues](https://img.shields.io/github/issues/henols/growatt-client.svg)](https://github.com/henols/growatt-client/issues/)

Python wrapper for getting data asynchronously from Growatt inverters via serial usb RS232 connection and modbus RTU protocol.

The Growatt inverted must support the modbus protocol (some older inverters only support proprietary serial communication)
Connect the RS232 DB9 usb adapter to the RS232 port on the underside of the inverter (you might have to remove a cover plate).

## Attributes

Depending on the firmware version of your inverter, not all attributes might be available

### Inverter properties
- serial_number
- model_number
- firmware

### Supprted attributes
<!-- attr-start -->

| Attribute | Register | Unit | Description | Misc |
| --- | ---: | --- | --- | --- |
| battery_charge | 1011 | kW | Battery charging |  |
| battery_charge_lifetime | 1058 | kWh | Battery charged total |  |
| battery_charge_today | 1056 | kWh | Battery charged today |  |
| battery_discharge | 1009 | kW | Battery discharging |  |
| battery_discharge_lifetime | 1054 | kWh | Battery discharged total |  |
| battery_discharge_today | 1052 | kWh | Battery discharged today |  |
| battery_voltage | 1013 | V | Battery voltage |  |
| consumption | Calc | kW | Consumption | {solar_generation} + {battery_discharge} + {import_from_grid} - {export_to_grid} - {battery_charge} |
| consumption_lifetime | Calc | kWh | Consumption total | {solar_generation_lifetime} + {battery_discharge_lifetime} + {import_from_grid_lifetime} - {export_to_grid_lifetime} - {battery_charge_lifetime} |
| consumption_today | Calc | kWh | Consumption today | {solar_generation_today} + {battery_discharge_today} + {import_from_grid_today} - {export_to_grid_today} - {battery_charge_today} |
| export_to_grid | 1029 | kW | Export to grid |  |
| export_to_grid_lifetime | 1050 | kWh | Export to grid total |  |
| export_to_grid_today | 1048 | kWh | Export to grid today |  |
| grid_frequency | 37 | Hz | Grid frequency |  |
| grid_voltage | 38 | V | Grid voltage |  |
| import_from_grid | 1021 | kW | Import from grid |  |
| import_from_grid_lifetime | 1046 | kWh | Import from grid total |  |
| import_from_grid_today | 1044 | kWh | Import from grid today |  |
| inverter_temperature1 | 93 | °C | Inverter temperature |  |
| inverter_temperature2 | 94 | °C | The inside IPM in inverter Temperature |  |
| inverter_temperature3 | 1040 | °C | Battery temperature |  |
| local_load | 1037 | kW | Inverter local load |  |
| local_load_lifetime | 1062 | kWh | Inverter local load total |  |
| local_load_today | 1060 | kWh | Inverter local load today |  |
| pv1 | 5 | kW | PV1 |  |
| pv1_lifetime | 61 | kWh | PV1 total |  |
| pv1_today | 59 | kWh | PV1 today |  |
| pv1_voltage | 3 | V | PV1 voltage |  |
| pv2 | 9 | kW | PV2 |  |
| pv2_lifetime | 65 | kWh | PV2 total |  |
| pv2_today | 63 | kWh | PV2 today |  |
| pv2_voltage | 7 | V | PV2 voltage |  |
| solar_generation | 1 | kW | All PV generation |  |
| solar_generation_lifetime | 91 | kWh | All PV generation total |  |
| solar_generation_today | Calc | kWh | All PV generation today | {pv2_today} + {pv1_today} |
| statement_of_charge | 1014 | % | Statement of charge |  |
| system_production_lifetime | 1139 | kWh | System production total |  |
| system_production_today | 1137 | kWh | System production today |  |

<!-- attr-end -->

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
