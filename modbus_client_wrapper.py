import logging
from sys import stdout
from pyModbusTCP.client import ModbusClient
from typing import List, Dict, Union
from enum import Enum


LOG = logging.getLogger(__name__)


class ModbusNumberMap(Enum):
    COILS = 0
    DISCRETE_INPUTS = 1
    HOLDING_REGISTERS = 4 #function 0x03 (read holding registers)
    INPUT_REGISTERS = 3 #function 0x04 (read input registers)


class ModbusClientWrapper(ModbusClient):

    COILS_MAX_READ_SIZE = 2000
    DISCRETE_INPUTS_MAX_READ_SIZE = 2000
    HOLDING_REGISTERS_MAX_READ_SIZE = 125
    INPUT_REGISTERS_MAX_READ_SIZE = 125

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)

    def read(self, modbus_number_list: list) -> Dict[int, Union[bool, int, None]]: 
        coils_read_list = [
            number for number in modbus_number_list if ModbusClientWrapper.get_function(number) == ModbusNumberMap.COILS.name
            ]
        discrete_input_read_list = [
            number for number in modbus_number_list if ModbusClientWrapper.get_function(number) == ModbusNumberMap.DISCRETE_INPUTS.name
            ]
        holding_registers_read_list = [
            number for number in modbus_number_list if ModbusClientWrapper.get_function(number) == ModbusNumberMap.HOLDING_REGISTERS.name
            ]
        input_registers_read_list = [
            number for number in modbus_number_list if ModbusClientWrapper.get_function(number) == ModbusNumberMap.INPUT_REGISTERS.name
            ]
        
        LOG.debug(f"found coils: {coils_read_list}")
        LOG.debug(f"found discrete_input: {discrete_input_read_list}")
        LOG.debug(f"found holding_registers: {holding_registers_read_list}")
        LOG.debug(f"found input registers: {input_registers_read_list}")

        coils_read_list_values = self.read_multi_coils(coils_read_list, return_dict=True)
        discrete_inputs_list_values = self.read_multi_discrete_inputs(discrete_input_read_list, return_dict=True)
        holding_registers_read_list_values = self.read_multi_holding_registers(holding_registers_read_list, return_dict=True)
        input_registers_read_list_values = self.read_multi_input_registers(input_registers_read_list, return_dict=True)

        return coils_read_list_values | discrete_inputs_list_values | holding_registers_read_list_values | input_registers_read_list_values


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
    def get_address(number):
        number_in_string = str(number)
        if 65536 >= number >= 1:
            address = number - 1
            return address
        else:
            number_without_function = int(number_in_string[1:])
            address = number_without_function - 1
            return address

    @staticmethod
    def get_function(number: int):
        number_in_string = str(number)
        function_number = int(number_in_string[0])
        if 65536 >= number >= 1:
            return ModbusNumberMap.COILS.name
        elif function_number == ModbusNumberMap.DISCRETE_INPUTS.value:
            return ModbusNumberMap.DISCRETE_INPUTS.name
        elif function_number == ModbusNumberMap.HOLDING_REGISTERS.value:
            return ModbusNumberMap.HOLDING_REGISTERS.name
        elif function_number == ModbusNumberMap.INPUT_REGISTERS.value:
            return ModbusNumberMap.INPUT_REGISTERS.name
        else:
            raise Exception("Modbus function unknown")

    @staticmethod
    def _create_reads(
            addresses: List[int], 
            max_read_size: int = 1, 
            read_mask: int = 65535
            ) -> List[List[int]]:
        coils_read = []
        done_list = set()
        addresses  = sorted(addresses)

        for i in range(len(addresses)):
            if addresses[i] not in done_list:

                read_size = 1
                remain_coils = addresses[i+1:]
                for remain_coil in remain_coils:
                    prev_elemet_diff = remain_coil - addresses[i]
                    if (
                        prev_elemet_diff <= read_mask 
                        and prev_elemet_diff + 1 <= max_read_size
                    ):
                            read_size = prev_elemet_diff + 1
                            done_list.add(remain_coil)
                    read_mask +=1

                coils_read.append([addresses[i], read_size])

        return coils_read

    def _read_multi(
            self, 
            numbers, 
            function, 
            max_read_size: int = 1, 
            read_mask: int = 65535, 
            return_dict: bool = False
            ):
        function_string = function.__doc__.splitlines()[0]

        if len(set(numbers)) != len(numbers):
            return Exception("provided list contains duplicates")
        
        LOG.debug(f"{function_string} to read modbus numbers: {numbers}")

        address_list = [ModbusClientWrapper.get_address(number) for number in numbers]
        LOG.debug(f"{function_string} to read modbus addresses: {address_list}")

        reads = ModbusClientWrapper._create_reads(address_list, max_read_size, read_mask)

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
