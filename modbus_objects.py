import modbus_function_code
from dataclasses import dataclass
from typing import Union


@dataclass
class ModbusFunctionCode:
    read: Union[int, hex]
    write: Union[int, hex] = None
    multi_write: Union[int, hex] = None


class ModbusObject:
    """Modbus object basic class"""

    def __init__(self, modbus_number: int, value_to_write: Union[int, bool] = None):
        self.number = modbus_number
        self.value_to_write = value_to_write
        self.read_value = None

    def __repr__(self):
        return str(self.number)

    @property
    def address(self):
        "Method to obtain address from modbus object number"
        first_modbus_number = self.MOBUS_NUMBER_RANGE[0]
        return self.number - first_modbus_number
    
    
    def update_value(self, value: Union[int, bool] = None):
        self.read_value = value


class Coil(ModbusObject):
    """Coil modbus object """
    MOBUS_NUMBER_RANGE = range(1,65537)
    VALUES = MOBUS_NUMBER_RANGE
    FUNCTION_CODE = ModbusFunctionCode(
        modbus_function_code.READ_COILS,
        modbus_function_code.WRITE_SINGLE_COIL,
        modbus_function_code.WRITE_MULTIPLE_COILS
    )


class DiscreteInput(ModbusObject):
    """Discrete Input modbus object """
    MOBUS_NUMBER_RANGE = range(100001,165537)
    VALUES = MOBUS_NUMBER_RANGE
    FUNCTION_CODE = ModbusFunctionCode(
        modbus_function_code.READ_DISCRETE_INPUTS,
    )


class InputRegister(ModbusObject):
    """Input Register modbus object """
    MOBUS_NUMBER_RANGE = range(300001,365537)
    VALUES = MOBUS_NUMBER_RANGE
    FUNCTION_CODE = ModbusFunctionCode(
        modbus_function_code.READ_INPUT_REGISTERS,
    )


class HoldingRegister(ModbusObject):
    """Holding Register modbus object """
    MOBUS_NUMBER_RANGE = range(400001,465537)
    VALUES = MOBUS_NUMBER_RANGE
    FUNCTION_CODE = ModbusFunctionCode(
        modbus_function_code.READ_HOLDING_REGISTERS,
        modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER,
        modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS,
    )





