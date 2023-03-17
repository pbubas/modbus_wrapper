from dataclasses import dataclass
from typing import List, Dict, Type, Union
from helper import ModbusObject
from modbus_objects import ModbusFunctionCode

class ModbusObjectListUniqueException(Exception):
    pass

@dataclass
class ModbusObjectList:
    type: Type
    objects: List[ModbusObject]

    def __post_init__(self):
        for obj in self.objects:
            if type(obj) != self.type:
                raise ModbusObjectListUniqueException(f'Modbus object {obj} is not type of {self.objects_type}')


    @classmethod
    def get_single_type_objects(cls, modbus_objects: List[ModbusObject]) -> list:
        modbus_object_types = list({type(i) for i in modbus_objects})
        list_to_return = []
        for object_type in modbus_object_types:
            is_type = lambda obj: type(obj)==object_type
            single_type_modbus_objects = list(filter(is_type, modbus_objects))
            list_to_return.append(
                cls(object_type, single_type_modbus_objects)
            )
        return list_to_return



@dataclasss
class ReadFunctionArgument:
    starting_address: int
    size: int
    object_list: List[ModbusObjectList] = None

    @classmethod
    def get_arguments(
            cls,
            modbus_objects: List[ModbusObject], 
            max_read_size: int = 1, 
            read_mask: int = 1
    ) -> list:
        """Function to get read arguments for modbus function from Modbus Objects"""

        single_type_obj_list = ModbusObjectList.get_single_type_objects(modbus_objects)
        for single_type in single_type_obj_list:
            arguments = []
            done_list = set()
            addresses = (obj.address for obj in single_type.objects)
            addresses  = sorted(addresses)

            for i in range(len(addresses)):
                if addresses[i] not in done_list:

                    read_size = 1
                    remain_coils = addresses[i+1:]
                    _read_mask = read_mask
                    for remain_coil in remain_coils:
                        prev_elemet_diff = remain_coil - addresses[i]
                        if (
                            prev_elemet_diff <= _read_mask 
                            and prev_elemet_diff + 1 <= max_read_size
                        ):
                                read_size = prev_elemet_diff + 1
                                done_list.add(remain_coil)
                        _read_mask +=1

                    argument = cls(addresses[i], read_size, single_type)
                    arguments.append(argument)

        return arguments

@dataclass
class WriteFunctionArgument:
    values_to_write: List[int] = None

     
    def get_arguments(modbus_objects: List[ModbusObject]):
        """Function to get read arguments for modbus function from Modbus Objects"""

        arguments = ModbusClientWrapper._get_modbus_function_args(modbus_objects, max_read_size=write_size, read_mask=1)

        
        