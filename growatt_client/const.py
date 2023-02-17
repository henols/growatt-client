"""Constants for GrowattClient library."""

# Defaults
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_ADDRESS = 0x1

# Word type
INT_BYTE = "int_byte"
SINGLE_BYTE = "single_byte"
DOUBLE_BYTE = "double_byte"

# Unit of measurement
ELECTRICAL_POTENTIAL_VOLT = "V"
ELECTRICAL_CURRENT_AMPERE = "A"
POWER_KILO_WATT = "kW"
REACTIVE_POWER_VAR = "var"
TIME_HOURS = "h"
ENERGY_KILO_WATT_HOUR = "kWh"
REACTIVE_ENERGY_KILO_VAR_HOUR = "kvarh"
FREQUENCY_HERTZ = "Hz"
TEMP_CELSIUS = "°C"


def create_value(name, pos, unit, desc, type=DOUBLE_BYTE, scale=0.1):
    return {
        "name": name,
        "pos": pos,
        "type": type,
        "unit": unit,
        "description": desc,
        "scale": scale,
    }


def create_template(name, unit, desc, template):
    """Creates a nice template value"""
    template = " ".join(template.split())
    value = {
        "name": name,
        "unit": unit,
        "description": desc,
        "template": template,
    }
    return value


def group_values(values):
    values.sort(key=lambda x: x["pos"])
    groups = []
    pos = -200

    for value in values:
        if pos + 100 < value["pos"] or (pos < 0 and value["pos"] >= 0):
            pos = value["pos"]
            group_list = []
            group = {}
            group["pos"] = pos
            group["values"] = group_list
            groups.append(group)
        group_list.append(value)
        group["length"] = (
            value["pos"] - pos + (2 if value["type"] == DOUBLE_BYTE else 1)
        )
    return groups


ATTRIBUTES = [
    create_value("pv1", 5, POWER_KILO_WATT, "PV1", DOUBLE_BYTE, 0.0001),
    create_value(
        "pv1_voltage",
        3,
        ELECTRICAL_POTENTIAL_VOLT,
        "PV1 voltage",
        SINGLE_BYTE,
    ),
    create_value(
        "pv1_today",
        59,
        ENERGY_KILO_WATT_HOUR,
        "PV1 today",
    ),
    create_value(
        "pv1_lifetime",
        61,
        ENERGY_KILO_WATT_HOUR,
        "PV1 total",
    ),
    create_value("pv2", 9, POWER_KILO_WATT, "PV2", DOUBLE_BYTE, 0.0001),
    create_value(
        "pv2_voltage",
        7,
        ELECTRICAL_POTENTIAL_VOLT,
        "PV2 voltage",
        SINGLE_BYTE,
    ),
    create_value(
        "pv2_today",
        63,
        ENERGY_KILO_WATT_HOUR,
        "PV2 today",
    ),
    create_value(
        "pv2_lifetime",
        65,
        ENERGY_KILO_WATT_HOUR,
        "PV2 total",
    ),
    create_value(
        "solar_generation",
        1,
        POWER_KILO_WATT,
        "All PV generation",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "solar_generation_lifetime",
        91,
        ENERGY_KILO_WATT_HOUR,
        "All PV generation total",
    ),
    # Battery
    create_value(
        "statement_of_charge",
        1014,
        "%",
        "Statement of charge",
        INT_BYTE,
        1,
    ),
    create_value(
        "battery_voltage",
        1013,
        ELECTRICAL_POTENTIAL_VOLT,
        "Battery voltage",
        SINGLE_BYTE,
    ),
    create_value(
        "battery_charge",
        1011,
        POWER_KILO_WATT,
        "Battery charging",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "battery_charge_today",
        1056,
        ENERGY_KILO_WATT_HOUR,
        "Battery charged today",
    ),
    create_value(
        "battery_charge_lifetime",
        1058,
        ENERGY_KILO_WATT_HOUR,
        "Battery charged total",
    ),
    create_value(
        "battery_discharge",
        1009,
        POWER_KILO_WATT,
        "Battery discharging",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "battery_discharge_today",
        1052,
        ENERGY_KILO_WATT_HOUR,
        "Battery discharged today",
    ),
    create_value(
        "battery_discharge_lifetime",
        1054,
        ENERGY_KILO_WATT_HOUR,
        "Battery discharged total",
    ),
    # Load consumtion
    create_value(
        "local_load",
        1037,
        POWER_KILO_WATT,
        "Inverter local load",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "local_load_today",
        1060,
        ENERGY_KILO_WATT_HOUR,
        "Inverter local load today",
    ),
    create_value(
        "local_load_lifetime",
        1062,
        ENERGY_KILO_WATT_HOUR,
        "Inverter local load total",
    ),
    # Export to grid
    create_value(
        "export_to_grid",
        1029,
        POWER_KILO_WATT,
        "Export to grid",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "export_to_grid_today",
        1048,
        ENERGY_KILO_WATT_HOUR,
        "Export to grid today",
    ),
    create_value(
        "export_to_grid_lifetime",
        1050,
        ENERGY_KILO_WATT_HOUR,
        "Export to grid total",
    ),
    # Import from grid
    create_value(
        "import_from_grid",
        1021,
        POWER_KILO_WATT,
        "Import from grid",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        "import_from_grid_today",
        1044,
        ENERGY_KILO_WATT_HOUR,
        "Import from grid today",
    ),
    create_value(
        "import_from_grid_lifetime",
        1046,
        ENERGY_KILO_WATT_HOUR,
        "Import from grid total",
    ),
    create_value(
        "system_production_today",
        1137,
        ENERGY_KILO_WATT_HOUR,
        "System production today",
    ),
    create_value(
        "system_production_lifetime",
        1139,
        ENERGY_KILO_WATT_HOUR,
        "System production total",
    ),
    create_value(
        "grid_voltage",
        38,
        ELECTRICAL_POTENTIAL_VOLT,
        "Grid voltage",
        SINGLE_BYTE,
    ),
    # create_value(
    #     "extra_inverter_power_today",
    #     1133,
    #     ENERGY_KILO_WATT_HOUR,
    #     "Extra inverter Power today",
    # ),
    # create_value(
    #     "extra_inverter_power_lifetime",
    #     1135,
    #     ENERGY_KILO_WATT_HOUR,
    #     "Extra inverter Power total",
    # ),
    create_value(
        "grid_frequency",
        37,
        FREQUENCY_HERTZ,
        "Grid frequency",
        SINGLE_BYTE,
        0.01
    ),
    create_value(
        "inverter_temperature1",
        93,
        TEMP_CELSIUS,
        "Inverter temperature",
        SINGLE_BYTE,
    ),
    create_value(
        "inverter_temperature2",
        94,
        TEMP_CELSIUS,
        "The inside IPM in inverter Temperature",
        SINGLE_BYTE,
    ),
    create_value(
        "inverter_temperature3",
        1040,
        TEMP_CELSIUS,
        "Battery temperature",
        SINGLE_BYTE,
    ),
]

ATTRIBUTES_GROUPED = group_values(ATTRIBUTES)


ATTRIBUTE_TEMPALTES = [
    create_template(
        "solar_generation_today",
        ENERGY_KILO_WATT_HOUR,
        "All PV generation today",
        "{pv2_today} + {pv1_today}",
    ),
    create_template(
        "consumption",
        POWER_KILO_WATT,
        "Consumption",
        "{solar_generation} + {battery_discharge} + {import_from_grid} - \
            {export_to_grid} - {battery_charge}",
    ),
    create_template(
        "consumption_today",
        ENERGY_KILO_WATT_HOUR,
        "Consumption today",
        "{solar_generation_today} + {battery_discharge_today} + \
            {import_from_grid_today} - {export_to_grid_today} - \
            {battery_charge_today}",
    ),
    create_template(
        "consumption_lifetime",
        ENERGY_KILO_WATT_HOUR,
        "Consumption total",
        "{solar_generation_lifetime} + {battery_discharge_lifetime} + \
            {import_from_grid_lifetime} - {export_to_grid_lifetime} - \
            {battery_charge_lifetime}",
    ),
]
