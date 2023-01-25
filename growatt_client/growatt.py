"""
Python wrapper for getting data asynchronously from Growatt inverters
via serial usb RS232/RS485 connection and modbus RTU protocol.
"""
import logging
import os

from datetime import datetime
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from .const import (
    DEFAULT_ADDRESS,
    DEFAULT_PORT,
    INT_BYTE,
    SINGLE_BYTE,
    DOUBLE_BYTE,
    ATTRIBUTES,
    ATTRIBUTES_GROUPED,
)


def get_from_single_byte(rr, index, scale=0.1):
    """Read and scale single to float."""
    return round(float(rr.registers[index]) * scale, 1)


def get_from_double_byte(rr, index, scale=0.1):
    """Read and scale double to float."""
    return round(
        float((rr.registers[index] << 16) + rr.registers[index + 1]) * scale, 1
    )


def get_byte(rr, index):
    return rr.registers[index]


def get_value(res, index, type, scale):
    if type == INT_BYTE:
        return get_byte(res, index)
    if type == SINGLE_BYTE:
        return get_from_single_byte(res, index, scale)
    if type == DOUBLE_BYTE:
        return get_from_double_byte(res, index, scale)
    return 0


def get_calculated_value(name):
    if name == "last_update":
        return datetime.now().timestamp()

    return None


class GrowattClient:
    """Main class to communicate with the Growatt inverter."""

    def __init__(
        self, port=DEFAULT_PORT, address=DEFAULT_ADDRESS, logger=None
    ):
        """Initialize."""
        if logger is None:
            self._logger = logging.getLogger(__name__)
            self._logger.addHandler(logging.NullHandler())
        else:
            self._logger = logger

        # usb port
        self._port = port
        # Modbus address (1-247)
        self._unit = address
        # Modbus serial rtu communication client
        self._client = ModbusClient(
            method="rtu",
            port=port,
            baudrate=9600,
            stopbits=1,
            parity="N",
            bytesize=8,
            timeout=1,
        )

        self._logger.debug(
            (
                f"GrowattClient initialized with usb port {self._port} "
                f"and modbus address {self._unit}."
            )
        )

    async def async_update(self):
        """
        Read Growatt data.

        Modbus rtu information from
        "Growatt PV Inverter Modbus RS485 RTU Protocol V3.14 2016-09-27".
        The availability of the attributes depends
        on the firmware version of your inverter.
        """

        data = {}

        if not os.path.exists(self._port):
            self._logger.debug(f"USB port {self._port} is not available")
            raise PortException(f"USB port {self._port} is not available")

        self._client.timeout = True
        if not self._client.connect():
            self._logger.debug(
                f"Modbus connection failed for address {self._unit}."
            )
            raise ModbusException(
                f"Modbus connection failed for address {self._unit}."
            )

        for group in ATTRIBUTES_GROUPED:
            pos = group["pos"]
            values = group["values"]
            self._logger.debug(group)

            if pos < 0:
                for value in values:
                    data[value["name"]] = get_calculated_value(value["name"])
                continue

            registers = self._client.read_input_registers(
                pos, group["length"], unit=self._unit
            )
            if registers.isError():
                self._client.close()
                self._logger.debug(f"Modbus read failed for registers {pos}.")
                raise ModbusException(
                    f"Modbus read failed for registers {pos}."
                )
            for value in values:
                val = get_value(
                    registers,
                    value["pos"] - pos,
                    value["type"],
                    value["scale"],
                )
                data[value["name"]] = val

        self._client.close()

        if not data:
            return {}

        return data

    def get_attributes(self):
        return ATTRIBUTES

    def get_attribute(self, name):
        for a in ATTRIBUTES:
            if a["name"] == name:
                return a


class PortException(Exception):
    """Raised when the USB port in not available."""

    def __init__(self, status):
        """Initialize."""
        super(PortException, self).__init__(status)
        self.status = status


class ModbusException(Exception):
    """Raised when the Modbus communication has error."""

    def __init__(self, status):
        """Initialize."""
        super(ModbusException, self).__init__(status)
        self.status = status
