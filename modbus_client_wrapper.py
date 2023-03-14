import logging
from sys import stdout
from pyModbusTCP.client import ModbusClient
from typing import List, Dict, Union
from enum import Enum
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
from modbus_address import ModbusListByType, ModbusAddress, ModbusList


LOG = logging.getLogger(__name__)


class ModbusClientWrapper(ModbusClient):

    COILS_MAX_READ_SIZE = 2000
    DISCRETE_INPUTS_MAX_READ_SIZE = 2000
    HOLDING_REGISTERS_MAX_READ_SIZE = 125
    INPUT_REGISTERS_MAX_READ_SIZE = 125

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.function_map = {
            READ_COILS: self.read_multi_coils,
            READ_HOLDING_REGISTERS: self.read_multi_holding_registers,
            READ_DISCRETE_INPUTS: self.read_discrete_inputs,
            READ_INPUT_REGISTERS: self.read_multi_input_registers,
            WRITE_SINGLE_COIL: self.write_single_coil,
            WRITE_SINGLE_HOLDING_REGISTER: self.write_single_register,
            WRITE_MULTIPLE_COILS: self.write_multiple_coils,
            WRITE_MULTIPLE_HOLDING_REGISTERS: self.write_multiple_registers
         }

    def read(self, modbus_number_list: list) -> Dict[int, Union[bool, int, None]]: 

        modbus_number_list = ModbusListByType(modbus_number_list)

        result = {}

        for values in modbus_number_list.data.values():
            read_function = self.function_map[values.function.read]
            result = result | read_function(values.numbers, return_dict=True)
        
        return result
    
    def write(self, modbus_dict_to_write: dict):
        modbus_list = ModbusListByType(list(modbus_dict_to_write.keys()))

        modbus_lists_of_one_type = modbus_list.data.values()

        for modbus_list in modbus_lists_of_one_type:
            self._write_modbus_list(modbus_list, modbus_dict_to_write)


    def _write_modbus_list(self, modbus_list: ModbusList, modbus_dict_to_write: dict):
            write_function = self.function_map[modbus_list.function.write]
            multi_write_function = self.function_map[modbus_list.function.multi_write]

            dict_to_write = {modbus.number:modbus_dict_to_write[modbus.number] for modbus in  modbus_list}
            arguments_to_write = self._create_writes(dict_to_write)

            for argument in arguments_to_write:
                if isinstance(argument[1], list):
                    print (f"write {argument} using {multi_write_function} \n")
                else:
                    print (f"write {argument} using {write_function} \n")

    @staticmethod
    def _create_writes(modbus_numbers_to_write: dict) -> dict:
        keys = modbus_numbers_to_write.keys()
        max_write_size=ModbusClientWrapper.HOLDING_REGISTERS_MAX_READ_SIZE

        writes = ModbusClientWrapper._create_reads(keys, max_read_size=max_write_size, read_mask=1)
        
        for i in writes:
            starting_address = i[0]
            write_size = i[1]
            addresses_to_write = range(starting_address, starting_address + write_size)

            values_to_write = [modbus_numbers_to_write[w] for w in addresses_to_write]
            number_of_values_to_write = len(values_to_write)
            values_to_write = int(values_to_write[0]) if number_of_values_to_write  == 1 else values_to_write

            i[1] = values_to_write

        return writes

        

    def read_multi_coils(self, coils_numbers: List[int], *args, **kwargs) -> Union[List[bool], Dict[int, bool]]:

        return self._read_multi(
            coils_numbers,
            self.read_coils,
            max_read_size = self.COILS_MAX_READ_SIZE,
            *args, **kwargs
            )


    def read_multi_discrete_inputs(self, discrete_inputs_numbers: List[int], *args, **kwargs):

        return self._read_multi(
            discrete_inputs_numbers,
            self.read_discrete_inputs,
            self.DISCRETE_INPUTS_MAX_READ_SIZE, 
            *args, **kwargs
            )


    def read_multi_holding_registers(self, holding_registers_numbers: List[int], *args, **kwargs):

        return self._read_multi(
            holding_registers_numbers,
            self.read_holding_registers,
            self.HOLDING_REGISTERS_MAX_READ_SIZE,
            *args, **kwargs
            )
    

    def read_multi_input_registers(self, input_registers_numbers: List[int], *args, **kwargs):

        return self._read_multi(
            input_registers_numbers,
            self.read_input_registers,
            self.INPUT_REGISTERS_MAX_READ_SIZE,
            *args, **kwargs
            )
    
    @staticmethod
    def _create_reads(
            addresses: List[int], 
            max_read_size: int = 1, 
            read_mask: int = 1
            ) -> List[List[int]]:
        coils_read = []
        done_list = set()
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


                coils_read.append([addresses[i], read_size])

        return coils_read

    def check_duplicates(self, list_to_check):
        if len(set(list_to_check)) != len(list_to_check):
            raise Exception("provided list contains duplicates")

    def _read_multi(
            self, 
            numbers, 
            function, 
            max_read_size: int = 1, 
            read_mask: int = 1, 
            return_dict: bool = False
            ):
        function_string = function.__doc__.splitlines()[0]
        
        self.check_duplicates(numbers)

        LOG.debug(f"{function_string} to read modbus numbers: {numbers}")

        address_list = [ModbusAddress.get_address(number) for number in numbers]
        LOG.debug(f"{function_string} to read modbus addresses: {address_list}")

        reads = ModbusClientWrapper._create_reads(address_list, max_read_size, read_mask)

        self.open()
        values = {}
        for read in reads:
            values[read[0]] = function(*read)
            if not values[read[0]]: # None means no reply from modbus target
                LOG.error(f'{function_string} failed to read {read}')
                values[read[0]] = [None for i in range(0, read[1])] # Fill all results with None, when no reply from Modbus target

            LOG.debug(f'{function_string} {read} results: {values[read[0]]}')
            increment = 0
            for value in values[read[0]]:
                values[read[0]+increment] = value
                increment+=1


        list_of_result_values = [values[entry] for entry in address_list]
        if return_dict:
            zip_with_number_and_values = zip(numbers, list_of_result_values)
            return dict(zip_with_number_and_values)

        return list_of_result_values
