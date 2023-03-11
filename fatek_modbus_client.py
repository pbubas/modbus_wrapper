import logging
from modbus_client_wrapper import ModbusClientWrapper
from fatek_address import FatekAddress, FatekList, fatek_mapping
from typing import Set

LOG = logging.getLogger(__name__)

class FatekAddressValidationError(Exception):
    pass

class FatekModbusClient:

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        self.client = ModbusClientWrapper(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.type_to_function = {
            "discret_srelays": self.read_discrete_inputs,
            "discret_mrelays": self.read_discrete_mrelays,
            "discret_inputs" : self.read_discrete_inputs,
            "discret_outputs" : self.read_discrete_outputs,
            "timers_status" : self.read_timers_status,
            "counters_status" : self.read_counter_status,
            "holding_registers" : self.read_holding_registers,
            "holding_registers_ror" : self.read_holding_registers_ror,
            "data_registers" : self.read_data_registers,
            "timers" : self.read_timers_data,
            "counters" : self.read_counters_data,
            "counters_32bit" : self.read_counters_32bit,
         }

    def read(self, fatek_addresses: set) -> dict():

        fatek_list = FatekList(fatek_addresses)

        result = {}

        for type, values in fatek_list.types.items():
            read_function = self.type_to_function[type]
            read_mask = len(fatek_mapping.MAP[type])
            result = result | read_function(values, read_mask, True) 
        
        return result
    
    def read_discrete_inputs(self, discrete_inputs: Set[FatekAddress], read_mask: int, return_dict: bool = False):

        return self._read_main(
            discrete_inputs, 
            self.client.read_multi_coils, 
            read_mask,
            return_dict
            )

    def read_discrete_outputs(self, discrete_outputs:  Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            discrete_outputs, 
            self.client.read_multi_coils, 
            read_mask, 
            return_dict
            )

    def read_discrete_mrelays(self, discrete_mrelays: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            discrete_mrelays, 
            self.client.read_multi_coils, 
            read_mask,
            return_dict
            )

    def read_discrete_srelays(self, discrete_srelays: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            discrete_srelays, 
            self.client.read_multi_coils, 
            read_mask,
            return_dict
            )

    def read_timers_status(self, timers: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            timers, 
            self.client.read_multi_coils, 
            read_mask,
            return_dict
            )

    def read_counter_status(self, counters: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            counters, 
            self.client.read_multi_coils, 
            read_mask, 
            return_dict
            )

    def read_holding_registers(self, holding_registers: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            holding_registers, 
            self.client.read_multi_holding_registers, 
            read_mask, 
            return_dict
            )

    def read_holding_registers_ror(self, holding_registers_ror: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            holding_registers_ror, 
            self.client.read_multi_holding_registers, 
            read_mask, 
            return_dict
            )

    def read_data_registers(self, data_registers: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            data_registers,
            self.client.read_multi_holding_registers, 
            read_mask, 
            return_dict
            )

    def read_timers_data(self, timers: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            timers,
            self.client.read_multi_holding_registers, 
            read_mask,
            return_dict
            )

    def read_counters_data(self, counters: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        return self._read_main(
            counters,
            self.client.read_multi_holding_registers, 
            read_mask,
            return_dict
            )

    def read_counters_32bit(self, counters_32bit: Set[FatekAddress], read_mask: int, return_dict: bool = False):
        pass

    def _read_main(self, fatek_addresses: Set[FatekAddress], function, read_mask: int, return_dict: bool = False):

        fatek_address_list = list(fatek_addresses)
        modbus_numbers = [address.modbus_number for address in fatek_address_list]
        fatek_addr_str = [address.address for address in fatek_address_list]


        self.client.open()
        modbus_values = function(modbus_numbers, read_mask=read_mask)

        if return_dict:
            dict_to_return =  dict(zip(fatek_addr_str, modbus_values))
            return dict_to_return
        return modbus_values





