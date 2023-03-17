import logging
from sys import stdout
from pyModbusTCP.client import ModbusClient
from typing import List, Dict, Union
import modbus_function_code 
from helper import ModbusObject, get_modbus_object
from dataclasses import dataclass
import modbus_objects

LOG = logging.getLogger(__name__)

class FunctionUnknow(Exception):
    pass


class ObjectNonWriteable(Exception):
    pass


@dataclass
class ModbusFunctionArgument:
     starting_address: int
     size: int

@dataclass
class ModbusWriteFunctionArgument:
     starting_address: int
     values_to_write: List[int]
     

class ModbusClientWrapper(ModbusClient):

    MAX_READ_SIZE = {
        modbus_objects.Coil : 2000,
        modbus_objects.DiscreteInput : 2000,
        modbus_objects.HoldingRegister : 125,
        modbus_objects.InputRegister : 125,
    }

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.function_map = {
            modbus_function_code.READ_COILS: self.read_coils,
            modbus_function_code.READ_HOLDING_REGISTERS: self.read_holding_registers,
            modbus_function_code.READ_DISCRETE_INPUTS: self.read_discrete_inputs,
            modbus_function_code.READ_INPUT_REGISTERS: self.read_input_registers,
            modbus_function_code.WRITE_SINGLE_COIL: self.write_single_coil,
            modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER: self.write_single_register,
            modbus_function_code.WRITE_MULTIPLE_COILS: self.write_multiple_coils,
            modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS: self.write_multiple_registers
         }
        
    def read(self, modbus_numbers: List[Union[int,str]], *args, **kwargs) -> dict:
        modbus_objects = [get_modbus_object(i) for i in modbus_numbers]

        modbus_objects = self.read_modbus_objects(modbus_objects, *args, **kwargs)

        result = {obj:obj.read_value for obj in modbus_objects}

        return result
    
    def read_modbus_objects(
            self, 
            modbus_objects: List[ModbusObject],  
            max_read_size: int = 1, 
            read_mask: int = 1,
            ) -> List[ModbusObject]:
        
        self._check_duplicates(modbus_objects)

        modbus_object_types = list({type(i) for i in modbus_objects})

        for object_type in modbus_object_types:
            function_code = object_type.FUNCTION_CODE.read
            read_function = self._get_function(function_code)
            function_string = read_function.__doc__.splitlines()[0]
            object_max_read_size = self._get_read_size(object_type) 
            _max_read_size = object_max_read_size if object_max_read_size else max_read_size

            objects_to_read = self._filter_modbus_type(object_type, modbus_objects)
            
            object_numbers = [object for object in objects_to_read]
            LOG.debug(f"{function_string} to read numbers: {object_numbers}")
            addresses_to_read = [object.address for object in objects_to_read]
            LOG.debug(f"{function_string} to read modbus addresses: {addresses_to_read}")

            function_arguments = self._get_modbus_function_args(objects_to_read, _max_read_size, read_mask)
            
            collected_values = self._read(function_arguments, read_function)

            [obj.update_value(collected_values[obj.address]) for obj in objects_to_read]

        return modbus_objects

    def write_modbus_objects(self, modbus_objects: List[ModbusObject]):
        modbus_object_types = list({type(i) for i in modbus_objects})
        for object_type in modbus_object_types:

            write_function_code = object_type.FUNCTION_CODE.write
            multi_write_function_code = object_type.FUNCTION_CODE.multi_write

            if not write_function_code or not multi_write_function_code:
                raise ObjectNonWriteable(f"object {object_type} is non writeable")

            write_function = self._get_function(write_function_code)
            multi_write_function = self._get_function(multi_write_function_code) 

            objects_to_write = self._filter_modbus_type(object_type, modbus_objects)
            write_size = self._get_read_size(object_type)
            arguments_to_write = self._get_modbus_write_function_args(objects_to_write, write_size)  

            self._write(arguments_to_write, write_function, multi_write_function)

        return "dupa"
            

    def _write(self, arguments_to_write, write_function, multi_write_function):
        for argument in arguments_to_write:
            # print (write_function, multi_write_function, argument.starting_address, argument.size)
            # print (write_function, multi_write_function, argument.starting_address, argument.size)
            print (argument)
        
        
    def _get_function(self, code:[hex, int]):
        """Get modbus function by code"""
        try:
            function = self.function_map[code]
        except KeyError:
            raise FunctionUnknow(f"code {code} not valid")
        
        return function

    @staticmethod
    def _get_modbus_write_function_args(modbus_objects: List[ModbusObject], write_size):
        arguments = ModbusClientWrapper._get_modbus_function_args(modbus_objects, max_read_size=write_size, read_mask=1)
        all_values_to_write = {obj.address: obj.value_to_write for obj in modbus_objects}

        arguments_to_write = []
        
        for argument in arguments:
            ending_address = argument.starting_address + (argument.size)
            range_of_addresses = range(argument.starting_address, ending_address)
            if len(range_of_addresses) == 1:
                values_to_write = all_values_to_write[argument.starting_address]
            else:
                values_to_write = [all_values_to_write[address] for address in range_of_addresses]

            argument = ModbusWriteFunctionArgument(argument.starting_address, values_to_write)
            arguments_to_write.append(argument)
            
        return arguments_to_write

    @staticmethod
    def _get_modbus_function_args(
            modbus_objects: List[ModbusObject], 
            max_read_size: int = 1, 
            read_mask: int = 1
            ) -> List[ModbusFunctionArgument]:

        arguments = []
        done_list = set()
        addresses = (obj.address for obj in modbus_objects)
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

                argument = ModbusFunctionArgument(addresses[i], read_size)
                arguments.append(argument)

        return arguments

    def _check_duplicates(self, list_to_check):
        if len(set(list_to_check)) != len(list_to_check):
            raise Exception("provided list contains duplicates")


    def _filter_modbus_type(self, object_type: ModbusObject, modbus_objects: List[ModbusObject]) -> List[ModbusObject]:
        is_type = lambda obj: type(obj)==object_type
        objects_to_read = filter(is_type, modbus_objects)

        return list(objects_to_read)

    def _get_read_size(self, modbus_class):
        try: 
            return next(
                value for cls, value in self.MAX_READ_SIZE.items() 
                if issubclass(modbus_class, cls)
                )
        except StopIteration:
            return None
    

    def _read(self, modbus_function_arguments: List[ModbusFunctionArgument], read_function):
        function_string = read_function.__doc__.splitlines()[0]

        self.open()

        collected_values = {}

        for argument in modbus_function_arguments:
            starting_address = argument.starting_address

            collected_values.update(
                {
                starting_address: read_function(starting_address, argument.size)
                }
            )

            if not collected_values[starting_address]: # None means no reply from modbus target
                LOG.error(f'{function_string} failed to read {argument}')
                collected_values[starting_address] = [None for i in range(0, argument.size)] # Fill all results with None, when no reply from Modbus target

            LOG.debug(f'{function_string} {argument} results: {collected_values[starting_address]}')

            increment = 0
            for value in collected_values[starting_address]:
                collected_values[starting_address+increment] = value
                increment+=1

        return collected_values

    