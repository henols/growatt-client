# GrowattClient

[![PyPI][pypi-releases-shield]][pypi-releases]
[![GitHub issues](https://img.shields.io/github/issues/henols/growatt-client.svg)](https://github.com/henols/growatt-client/issues/)

Python wrapper for getting data asynchronously from Growatt inverters via serial RS232/RS485 connection and modbus RTU protocol.

The implementation is based on [Growatt Inverter Modbus RTU Protocol V1.20](docs/growatt-inverter-modbus-rtu-protocol-ii-series-modbus-growatt-inverter-modbus.pdf).


Tested with inverters:
 - SPH 10000 TL3 BH

## Attributes

Depending on the firmware version of your inverter, not all attributes might be available

### Holding register attributes
- serial_number
- model_number
- firmware

### Input register attributes
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
| consumption | Calc | kW | Consumption | {photovoltaics} + {battery_discharge} + {import_from_grid} - {export_to_grid} - {battery_charge} |
| consumption_lifetime | Calc | kWh | Consumption total | {photovoltaics_lifetime} + {battery_discharge_lifetime} + {import_from_grid_lifetime} - {export_to_grid_lifetime} - {battery_charge_lifetime} |
| consumption_today | Calc | kWh | Consumption today | {photovoltaics_today} + {battery_discharge_today} + {import_from_grid_today} - {export_to_grid_today} - {battery_charge_today} |
| export_to_grid | 1029 | kW | Export to grid |  |
| export_to_grid_lifetime | 1050 | kWh | Export to grid total |  |
| export_to_grid_today | 1048 | kWh | Export to grid today |  |
| grid_frequency | 37 | Hz | Grid frequency |  |
| grid_voltage | 38 | V | Grid voltage |  |
| import_from_grid | 1021 | kW | Import from grid |  |
| import_from_grid_lifetime | 1046 | kWh | Import from grid total |  |
| import_from_grid_today | 1044 | kWh | Import from grid today |  |
| inverter_temperature_1 | 93 | °C | Inverter temperature |  |
| inverter_temperature_2 | 94 | °C | The inside IPM in inverter Temperature |  |
| inverter_temperature_3 | 1040 | °C | Battery temperature |  |
| local_load | 1037 | kW | Inverter local load |  |
| local_load_lifetime | 1062 | kWh | Inverter local load total |  |
| local_load_today | 1060 | kWh | Inverter local load today |  |
| photovoltaics | 1 | kW | Photovoltaics (PV) generation |  |
| photovoltaics_1 | 5 | kW | Photovoltaics (PV) 1 |  |
| photovoltaics_1_lifetime | 61 | kWh | Photovoltaics (PV) 1 total |  |
| photovoltaics_1_today | 59 | kWh | Photovoltaics (PV) 1 today |  |
| photovoltaics_1_voltage | 3 | V | Photovoltaics (PV) 1 voltage |  |
| photovoltaics_2 | 9 | kW | Photovoltaics (PV) 2 |  |
| photovoltaics_2_lifetime | 65 | kWh | Photovoltaics (PV) 2 total |  |
| photovoltaics_2_today | 63 | kWh | Photovoltaics (PV) 2 today |  |
| photovoltaics_2_voltage | 7 | V | Photovoltaics (PV) 2 voltage |  |
| photovoltaics_lifetime | 91 | kWh | Photovoltaics (PV) generation total |  |
| photovoltaics_today | Calc | kWh | Photovoltaics (PV) generation today | {photovoltaics_2_today} + {photovoltaics_1_today} |
| self_consumption | Calc | kW | Self Consumption | {consumption} if {export_to_grid} > 0 else {system_production} |
| statement_of_charge | 1014 | % | Statement of charge (SOC), capacity |  |
| system_production | Calc | kW | System Production | {photovoltaics} + {battery_discharge} - {battery_charge} |
| system_production_lifetime | Calc | kWh | System Production total | {photovoltaics_lifetime} + {battery_discharge_lifetime} - {battery_charge_lifetime} |
| system_production_today | Calc | kWh | System Production today | {photovoltaics_today} + {battery_discharge_today} - {battery_charge_today} |
| system_production_with_battery_lifetime | 1139 | kWh | System production total (including battery) |  |
| system_production_with_battery_today | 1137 | kWh | System production today (including battery) |  |

<!-- attr-end -->

## How to use the package

```py
import asyncio
import logging
from sys import argv

from growatt_client.growatt import GrowattClient

# defaults
# USB port of RS232/RS485 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)


async def main():
    port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
    address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
    growatt_client = GrowattClient(
        port, 
        address,
        attributes=["import_from_grid_today", "local_load_lifetime"],
        )
        
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
