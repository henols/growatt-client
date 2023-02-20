"""
Python wrapper for getting data asynchronously from Growatt inverters
via serial usb RS232/RS485 connection and modbus RTU protocol.
"""
import logging
import os

from pymodbus.client.serial import AsyncModbusSerialClient as ModbusClient

from .const import (
    ATTRIBUTES,
    DEFAULT_ADDRESS,
    DEFAULT_PORT,
    DOUBLE_BYTE,
    INT_BYTE,
    SINGLE_BYTE,
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


def get_string(res, index, length):
    string = ""
    for pos in range(0, length):
        string += str(
            chr(res.registers[index + pos] >> 8)
            + chr(res.registers[index + pos] & 0x000000FF)
        )
    return string


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


class GrowattClient:
    """Main class to communicate with the Growatt inverter."""

    def __init__(
        self,
        port=DEFAULT_PORT,
        address=DEFAULT_ADDRESS,
        attributes=None,
        attribute_defs=ATTRIBUTES,
        logger=None,
    ):
        """Initialize."""
        if logger is None:
            self._logger = logging.getLogger(__name__)
            self._logger.addHandler(logging.NullHandler())
        else:
            self._logger = logger

        if attributes is not None:
            attribute_defs = []
            for attr_name in attributes:
                for a in ATTRIBUTES:
                    if a["name"] == attr_name:
                        attribute_defs.append(a)

        _attributes = []
        for attr in attribute_defs:
            if True if "pos" in attr else False:
                _attributes.append(attr)

        self.attributes = group_values(_attributes)

        self.templates = []
        for attr in attribute_defs:
            if True if "template" in attr else False:
                self.templates.append(attr)

        # usb port
        self._port = port
        self._address = address

        if not os.path.exists(self._port):
            self._logger.debug(f"USB port {self._port} is not available")
            raise PortException(f"USB port {self._port} is not available")

        # Modbus serial rtu communication client
        self._client = ModbusClient(
            port=port,
            baudrate=9600,
            stopbits=1,
            parity="N",
            bytesize=8,
            timeout=1,
        )

        self._serial_number = ""
        self._model_number = ""
        self._firmware = ""

        self._logger.debug(
            f"GrowattClient initialized with usb port {self._port}"
        )

    async def async_update(self):
        """
        Read Growatt data.

        Modbus rtu information from
        "Growatt Inverter Modbus RTU Protocol V1.20 2020-04-28".
        The availability of the attributes depends
        on the firmware version of your inverter.
        """

        data = {}
        await self.update_hardware_info()

        for group in self.attributes:
            pos = group["pos"]
            values = group["values"]
            self._logger.debug(group)

            if not await self._client.connect():
                self._logger.debug("Modbus connection failed.")
                raise ModbusException("Modbus connection failed.")

            registers = await self._client.read_input_registers(
                pos, group["length"], slave=self._address
            )

            if registers.isError():
                await self._client.close()
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

            await self._client.close()

        for value in self.templates:
            templ = value["template"].format_map(data)
            val = round(eval(templ), 1)
            self._logger.debug(
                "Converting template: %s \n -> to: %s = %f",
                value["template"],
                templ,
                val,
            )
            data[value["name"]] = val

        return data

    async def update_hardware_info(self):
        if self._serial_number == "":
            if not await self._client.connect():
                self._logger.debug("Modbus connection failed.")
                raise ModbusException("Modbus connection failed.")

            # Assuming the serial number doesn't change, it is read only once
            registers = await self._client.read_holding_registers(
                0, 30, slave=self._address
            )
            if registers.isError():
                await self._client.close()
                self._logger.debug("Modbus read failed for holding registers.")
                raise ModbusException(
                    "Modbus read failed for holding registers."
                )

            self._firmware = get_string(registers, 9, 3)
            self._serial_number = get_string(registers, 23, 5)

            mo = (registers.registers[28] << 16) + registers.registers[29]
            self._model_number = (
                "T"
                + str((mo & 0xF00000) >> 20)
                + " Q"
                + str((mo & 0x0F0000) >> 16)
                + " P"
                + str((mo & 0x00F000) >> 12)
                + " U"
                + str((mo & 0x000F00) >> 8)
                + " M"
                + str((mo & 0x0000F0) >> 4)
                + " S"
                + str((mo & 0x00000F))
            )

            self._logger.debug(
                (
                    f"Growatt serial number {self._serial_number} "
                    f"is model {self._model_number} "
                    f"and has firmware {self._firmware}."
                )
            )

            # Read time
            # self._logger.info(
            #     (
            #         f"{registers.registers[45]}-"
            #         f"{registers.registers[46]:02d}-"
            #         f"{registers.registers[47]:02d} "
            #         f"{registers.registers[48]:02d}:"
            #         f"{registers.registers[49]:02d}:"
            #         f"{registers.registers[50]:02d} "
            #         # f"day: {registers.registers[51]} "
            #     )
            # )

            await self._client.close()

    def get_attributes(self):
        return ATTRIBUTES

    def get_attribute(self, name):
        for a in self.get_attributes():
            if a["name"] == name:
                return a

    def get_serial_number(self):
        return self._serial_number

    def get_firmware(self):
        return self._firmware

    def get_model_number(self):
        return self._model_number


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
