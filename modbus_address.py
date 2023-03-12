from modbus_functions_map import (
        READ_COILS,
        READ_HOLDING_REGISTERS,
        READ_DISCRETE_INPUTS,
        READ_INPUT_REGISTERS,
        WRITE_SINGLE_COIL,
        WRITE_SINGLE_HOLDING_REGISTER,
        WRITE_MULTIPLE_COILS,
        WRITE_MULTIPLE_HOLDING_REGISTERS,
)
from dataclasses import dataclass
from typing import List, Union


@dataclass
class ModbusType:
    name: str
    read: int
    write: int = None
    multi_write: int = None

COILS = ModbusType(
    "coils",
    READ_COILS,
    WRITE_SINGLE_COIL,
    WRITE_MULTIPLE_COILS)
DISCRETE_INPUTS = ModbusType("discrete_inputs",READ_DISCRETE_INPUTS)
INPUT_REGISTERS = ModbusType("input_registers", READ_INPUT_REGISTERS)
HOLDING_REGISTERS = ModbusType(
    "holding_registers",
    READ_HOLDING_REGISTERS,
    WRITE_SINGLE_HOLDING_REGISTER,
    WRITE_MULTIPLE_HOLDING_REGISTERS
    )

NUMBER_PREFIX_MAP = {
    0 : COILS,
    1 : DISCRETE_INPUTS,
    3 : INPUT_REGISTERS,
    4 : HOLDING_REGISTERS
}

class ModbusNumberValidationException(Exception):
    pass

class ModbusAddress:
    def __init__(self, modbus_number: int):
        modbus_number = int(modbus_number)
        self.validate(modbus_number)

        self.number = modbus_number
        self.address = ModbusAddress.get_address(modbus_number)
        self.prefix = self.get_prefix(modbus_number)
        self.function = NUMBER_PREFIX_MAP[self.prefix]

    def validate(self, modbus_number):
        number_in_string = str(modbus_number)
        number_of_digits = len(number_in_string)
        prefix = int(number_in_string[0])
        allowed_prefixes = NUMBER_PREFIX_MAP.keys()
        exception = ModbusNumberValidationException(f"modbus number {modbus_number} out of range")

        if number_of_digits > 6:
            raise exception
        elif number_of_digits == 6 and not prefix in allowed_prefixes:
            raise exception
        elif number_of_digits < 6 and not (65536 >= modbus_number >= 1):
            raise exception

    @staticmethod
    def get_address(modbus_number):
        number_in_string = str(modbus_number)

        if len(number_in_string) == 6:
            return int(number_in_string[1:])
        return modbus_number
                   
    def get_prefix(self, modbus_number):
        number_in_string = str(modbus_number)

        if len(number_in_string) == 6:
            return int(number_in_string[0])
        return 0


class ModbusList(list):
    def __init__ (self, modbus_list: List[ModbusAddress]):
        super().__init__(modbus_list)

        all_types = {i.prefix for i in self}
        if len(all_types) != 1: 
            raise ModbusNumberValidationException(f"modbus numbers needs to be same type")
        
        self.prefix = self[0].prefix
        self.function = self[0].function

    @property
    def numbers(self):
        return [i.number for i in self]
    
    @property
    def addresses(self):
        return [i.address for i in self]


class ModbusListByType(list):
    def __init__ (self, modbus_list: Union[list,str,int]):
        if not isinstance(modbus_list, list):
            modbus_list = list([modbus_list])

        _modbus_list = []
        for entry in modbus_list:
            if "-" in str(entry):
                _modbus_list = _modbus_list + (self.convert_range(entry))
            else:
                _modbus_list.append(entry)

        modbus_list = [ModbusAddress(entry) for entry in _modbus_list]

        super().__init__(modbus_list)

        all_types = {entry.function.name for entry in self}

        for type in all_types:
            self.__dict__[type] = self._get_types(type)
            
    def _get_types(self, type_name: str):
        return ModbusList([entry for entry in self if entry.function.name == type_name])
    
    @property
    def data(self):
        return self.__dict__
    
    def convert_range(self, modbus_range: str):

        modbus_range = modbus_range.split("-")

        start_number = int(modbus_range[0])
        end_number = int(modbus_range[1]) + 1

        number_range = list(range(start_number, end_number))

        return number_range