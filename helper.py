from modbus_objects import ModbusObject
from fatek_objects import FatekObject
from typing import Union

class ModbusObjectValidation(Exception):
    pass

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def get_modbus_object(modbus_number: int, value_to_write: Union[int, bool] = None) -> ModbusObject:
    for object_class in all_subclasses(ModbusObject):
        if modbus_number in object_class.VALUES:
                return object_class(modbus_number, value_to_write)
    raise ModbusObjectValidation(f'provided number {modbus_number} is not valid Modbus object')

