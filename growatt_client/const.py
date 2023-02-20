"""Constants for GrowattClient library."""

# Defaults
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_ADDRESS = 0x1


PHOTOVOLTAICS_1 = "photovoltaics_1"
PHOTOVOLTAICS_1_VOLTAGE = "photovoltaics_1_voltage"
PHOTOVOLTAICS_1_TODAY = "photovoltaics_1_today"
PHOTOVOLTAICS_1_LIFETIME = "photovoltaics_1_lifetime"
PHOTOVOLTAICS_2 = "photovoltaics_2"
PHOTOVOLTAICS_2_VOLTAGE = "photovoltaics_2_voltage"
PHOTOVOLTAICS_2_TODAY = "photovoltaics_2_today"
PHOTOVOLTAICS_2_LIFETIME = "photovoltaics_2_lifetime"
PHOTOVOLTAICS = "photovoltaics"
PHOTOVOLTAICS_LIFETIME = "photovoltaics_lifetime"
STATEMENT_OF_CHARGE = "statement_of_charge"
BATTERY_VOLTAGE = "battery_voltage"
BATTERY_CHARGE = "battery_charge"
BATTERY_CHARGE_TODAY = "battery_charge_today"
BATTERY_CHARGE_LIFETIME = "battery_charge_lifetime"
BATTERY_DISCHARGE = "battery_discharge"
BATTERY_DISCHARGE_TODAY = "battery_discharge_today"
BATTERY_DISCHARGE_LIFETIME = "battery_discharge_lifetime"
LOCAL_LOAD = "local_load"
LOCAL_LOAD_TODAY = "local_load_today"
LOCAL_LOAD_LIFETIME = "local_load_lifetime"
EXPORT_TO_GRID = "export_to_grid"
EXPORT_TO_GRID_TODAY = "export_to_grid_today"
EXPORT_TO_GRID_LIFETIME = "export_to_grid_lifetime"
IMPORT_FROM_GRID = "import_from_grid"
IMPORT_FROM_GRID_TODAY = "import_from_grid_today"
IMPORT_FROM_GRID_LIFETIME = "import_from_grid_lifetime"
SYSTEM_PRODUCTION_WITH_BATTERY_TODAY = "system_production_with_battery_today"
SYSTEM_PRODUCTION_WITH_BATTERY_LIFETIME = (
    "system_production_with_battery_lifetime"
)
GRID_VOLTAGE = "grid_voltage"
GRID_FREQUENCY = "grid_frequency"
INVERTER_TEMPERATURE_1 = "inverter_temperature_1"
INVERTER_TEMPERATURE_2 = "inverter_temperature_2"
INVERTER_TEMPERATURE_3 = "inverter_temperature_3"
PHOTOVOLTAICS_TODAY = "photovoltaics_today"
CONSUMPTION = "consumption"
CONSUMPTION_TODAY = "consumption_today"
CONSUMPTION_LIFETIME = "consumption_lifetime"
SYSTEM_PRODUCTION = "system_production"
SYSTEM_PRODUCTION_TODAY = "system_production_today"
SYSTEM_PRODUCTION_LIFETIME = "system_production_lifetime"
SELF_CONSUMPTION = "self_consumption"

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


ATTRIBUTES = [
    create_value(
        PHOTOVOLTAICS_1,
        5,
        POWER_KILO_WATT,
        "Photovoltaics (PV) 1",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        PHOTOVOLTAICS_1_VOLTAGE,
        3,
        ELECTRICAL_POTENTIAL_VOLT,
        "Photovoltaics (PV) 1 voltage",
        SINGLE_BYTE,
    ),
    create_value(
        PHOTOVOLTAICS_1_TODAY,
        59,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) 1 today",
    ),
    create_value(
        PHOTOVOLTAICS_1_LIFETIME,
        61,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) 1 total",
    ),
    create_value(
        PHOTOVOLTAICS_2,
        9,
        POWER_KILO_WATT,
        "Photovoltaics (PV) 2",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        PHOTOVOLTAICS_2_VOLTAGE,
        7,
        ELECTRICAL_POTENTIAL_VOLT,
        "Photovoltaics (PV) 2 voltage",
        SINGLE_BYTE,
    ),
    create_value(
        PHOTOVOLTAICS_2_TODAY,
        63,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) 2 today",
    ),
    create_value(
        PHOTOVOLTAICS_2_LIFETIME,
        65,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) 2 total",
    ),
    create_value(
        PHOTOVOLTAICS,
        1,
        POWER_KILO_WATT,
        "Photovoltaics (PV) generation",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        PHOTOVOLTAICS_LIFETIME,
        91,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) generation total",
    ),
    # Battery
    create_value(
        STATEMENT_OF_CHARGE,
        1014,
        "%",
        "Statement of charge (SOC), capacity",
        INT_BYTE,
        1,
    ),
    create_value(
        BATTERY_VOLTAGE,
        1013,
        ELECTRICAL_POTENTIAL_VOLT,
        "Battery voltage",
        SINGLE_BYTE,
    ),
    create_value(
        BATTERY_CHARGE,
        1011,
        POWER_KILO_WATT,
        "Battery charging",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        BATTERY_CHARGE_TODAY,
        1056,
        ENERGY_KILO_WATT_HOUR,
        "Battery charged today",
    ),
    create_value(
        BATTERY_CHARGE_LIFETIME,
        1058,
        ENERGY_KILO_WATT_HOUR,
        "Battery charged total",
    ),
    create_value(
        BATTERY_DISCHARGE,
        1009,
        POWER_KILO_WATT,
        "Battery discharging",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        BATTERY_DISCHARGE_TODAY,
        1052,
        ENERGY_KILO_WATT_HOUR,
        "Battery discharged today",
    ),
    create_value(
        BATTERY_DISCHARGE_LIFETIME,
        1054,
        ENERGY_KILO_WATT_HOUR,
        "Battery discharged total",
    ),
    # Load consumtion
    create_value(
        LOCAL_LOAD,
        1037,
        POWER_KILO_WATT,
        "Inverter local load",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        LOCAL_LOAD_TODAY,
        1060,
        ENERGY_KILO_WATT_HOUR,
        "Inverter local load today",
    ),
    create_value(
        LOCAL_LOAD_LIFETIME,
        1062,
        ENERGY_KILO_WATT_HOUR,
        "Inverter local load total",
    ),
    # Export to grid
    create_value(
        EXPORT_TO_GRID,
        1029,
        POWER_KILO_WATT,
        "Export to grid",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        EXPORT_TO_GRID_TODAY,
        1048,
        ENERGY_KILO_WATT_HOUR,
        "Export to grid today",
    ),
    create_value(
        EXPORT_TO_GRID_LIFETIME,
        1050,
        ENERGY_KILO_WATT_HOUR,
        "Export to grid total",
    ),
    # Import from grid
    create_value(
        IMPORT_FROM_GRID,
        1021,
        POWER_KILO_WATT,
        "Import from grid",
        DOUBLE_BYTE,
        0.0001,
    ),
    create_value(
        IMPORT_FROM_GRID_TODAY,
        1044,
        ENERGY_KILO_WATT_HOUR,
        "Import from grid today",
    ),
    create_value(
        IMPORT_FROM_GRID_LIFETIME,
        1046,
        ENERGY_KILO_WATT_HOUR,
        "Import from grid total",
    ),
    create_value(
        SYSTEM_PRODUCTION_WITH_BATTERY_TODAY,
        1137,
        ENERGY_KILO_WATT_HOUR,
        "System production today (including battery)",
    ),
    create_value(
        SYSTEM_PRODUCTION_WITH_BATTERY_LIFETIME,
        1139,
        ENERGY_KILO_WATT_HOUR,
        "System production total (including battery)",
    ),
    create_value(
        GRID_VOLTAGE,
        38,
        ELECTRICAL_POTENTIAL_VOLT,
        "Grid voltage",
        SINGLE_BYTE,
    ),
    create_value(
        GRID_FREQUENCY,
        37,
        FREQUENCY_HERTZ,
        "Grid frequency",
        SINGLE_BYTE,
        0.01,
    ),
    create_value(
        INVERTER_TEMPERATURE_1,
        93,
        TEMP_CELSIUS,
        "Inverter temperature",
        SINGLE_BYTE,
    ),
    create_value(
        INVERTER_TEMPERATURE_2,
        94,
        TEMP_CELSIUS,
        "The inside IPM in inverter Temperature",
        SINGLE_BYTE,
    ),
    create_value(
        INVERTER_TEMPERATURE_3,
        1040,
        TEMP_CELSIUS,
        "Battery temperature",
        SINGLE_BYTE,
    ),
    create_template(
        PHOTOVOLTAICS_TODAY,
        ENERGY_KILO_WATT_HOUR,
        "Photovoltaics (PV) generation today",
        "{photovoltaics_2_today} + {photovoltaics_1_today}",
    ),
    create_template(
        CONSUMPTION,
        POWER_KILO_WATT,
        "Consumption",
        "{photovoltaics} + {battery_discharge} + {import_from_grid} - \
            {export_to_grid} - {battery_charge}",
    ),
    create_template(
        CONSUMPTION_TODAY,
        ENERGY_KILO_WATT_HOUR,
        "Consumption today",
        "{photovoltaics_today} + {battery_discharge_today} + \
            {import_from_grid_today} - {export_to_grid_today} - \
            {battery_charge_today}",
    ),
    create_template(
        CONSUMPTION_LIFETIME,
        ENERGY_KILO_WATT_HOUR,
        "Consumption total",
        "{photovoltaics_lifetime} + {battery_discharge_lifetime} + \
            {import_from_grid_lifetime} - {export_to_grid_lifetime} - \
            {battery_charge_lifetime}",
    ),
    create_template(
        SYSTEM_PRODUCTION,
        POWER_KILO_WATT,
        "System Production",
        "{photovoltaics} + {battery_discharge} - {battery_charge}",
    ),
    create_template(
        SYSTEM_PRODUCTION_TODAY,
        ENERGY_KILO_WATT_HOUR,
        "System Production today",
        "{photovoltaics_today} + {battery_discharge_today} - \
            {battery_charge_today}",
    ),
    create_template(
        SYSTEM_PRODUCTION_LIFETIME,
        ENERGY_KILO_WATT_HOUR,
        "System Production total",
        "{photovoltaics_lifetime} + {battery_discharge_lifetime} - \
            {battery_charge_lifetime}",
    ),
    create_template(
        SELF_CONSUMPTION,
        POWER_KILO_WATT,
        "Self Consumption",
        "{consumption} if {export_to_grid} > 0 else {system_production}",
    ),
]
