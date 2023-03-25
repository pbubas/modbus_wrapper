from dataclasses import dataclass
from typing import Union
from .. import modbus_function_code
from .config import MaxReadSize, ReadMask, MaxWriteSize
from .modbus_value import IntValue, BoolValue


@dataclass
class FunctionCode:
    read: Union[int, hex]
    write: Union[int, hex] = None
    multi_write: Union[int, hex] = None

@dataclass
class TargetRangeInt:
    low: int
    high: int


@dataclass
class TargetRangeBool:
    value : bool


class Int:
    """modbus 16bit integer object"""
    VALUE_READ_CLS = IntValue.from_unsign_int
    VALUE_WRITE_CLS = IntValue.from_sign_int


class Bool:
    """modbus bool object"""
    VALUE_READ_CLS = BoolValue.from_bool
    VALUE_WRITE_CLS = BoolValue.from_bool
    

class ModbusObject:
    """Modbus object basic class"""

    def __init__(
            self, modbus_number: int,
            value_to_write: int | bool = None,
            target_range: TargetRangeInt | TargetRangeBool = None
        ):
        self.number = modbus_number
        self.write_value = self.VALUE_WRITE_CLS(value_to_write)
        self.current_value = None
        self.target_range = target_range
        self._changed = None

    def __repr__(self):
        return str(self.number)

    @property
    def address(self):
        "Method to obtain address from modbus object number"
        first_modbus_number = self.MOBUS_NUMBER_RANGE[0]
        return self.number - first_modbus_number

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, change_bit: bool):
        self._changed = change_bit

    def update_current_value(self, value: int | bool | None):
        """method to update collected value, None values are ignored"""
        if value == None:
            self.changed = False
            self.current_value = None
            return None

        previous_value = self.current_value

        read_value_changed = all([previous_value != value, previous_value != None])
        read_value_unchanged = all([previous_value == value, previous_value != None])

        if read_value_changed:
            self.changed = True
        elif read_value_unchanged:
            self.changed = False

        self.current_value = self.VALUE_READ_CLS(value)
        return self.current_value


    def update_write_value(self, value_to_write: int | bool):
        self.value_to_write = self.VALUE_WRITE_CLS(value_to_write) if value_to_write else None
        return self.value_to_write




class Coil(ModbusObject, Bool):
    """Coil modbus object """
    MAX_READ_SIZE = MaxReadSize.COIL
    READ_MASK = ReadMask.COIL
    MAX_WRITE_SIZE = MaxWriteSize.COIL
    MOBUS_NUMBER_RANGE = range(1,65537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_COILS,
        modbus_function_code.WRITE_SINGLE_COIL,
        modbus_function_code.WRITE_MULTIPLE_COILS
    )


class DiscreteInput(ModbusObject, Bool):
    """Discrete Input modbus object """
    MAX_READ_SIZE = MaxReadSize.DISCRETE_INPUT
    READ_MASK = ReadMask.DISCRETE_INPUT
    MAX_READ_SIZE = 2000
    MOBUS_NUMBER_RANGE = range(100001,165537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_DISCRETE_INPUTS,
    )


class InputRegister(ModbusObject, Int):
    """Input Register modbus object """
    MAX_READ_SIZE = MaxReadSize.INPUT_REGISTER
    READ_MASK = ReadMask.INPUT_REGISTER
    MOBUS_NUMBER_RANGE = range(300001,365537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_INPUT_REGISTERS,
    )


class HoldingRegister(ModbusObject, Int):
    """Holding Register modbus object """
    MAX_READ_SIZE = MaxReadSize.HOLDING_REGISTER
    READ_MASK = ReadMask.HOLDING_REGISTER
    MAX_WRITE_SIZE = MaxWriteSize.HOLDING_REGISTER
    MOBUS_NUMBER_RANGE = range(400001,465537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_HOLDING_REGISTERS,
        modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER,
        modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS,
    )





