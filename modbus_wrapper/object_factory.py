from .objects import ModbusObject

class ModbusObjectValidation(Exception):
    pass

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])

def get_modbus_object(modbus_number: int, value_to_write: int | bool | None = None) -> ModbusObject:
    for object_class in all_subclasses(ModbusObject):
        if modbus_number in object_class.VALUES:
                return object_class(modbus_number, value_to_write)
    raise ModbusObjectValidation(f'provided number {modbus_number} is not valid Modbus object')

def get_modbus_object_from_range(number_range: str):
     pass
     