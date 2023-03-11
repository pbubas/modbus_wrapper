import logging
from modbus_client_wrapper import ModbusClientWrapper
from fatek_address import FatekByType, FatekList
from typing import Set

LOG = logging.getLogger(__name__)


class FatekModbusClient(ModbusClientWrapper):

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.type_to_function = {
            "discret_srelays": self.read_multi_coils,
            "discret_mrelays": self.read_multi_coils,
            "discret_inputs" : self.read_multi_coils,
            "discret_outputs" : self.read_multi_coils,
            "timers_status" : self.read_multi_coils,
            "counters_status" : self.read_multi_coils,
            "holding_registers" : self.read_multi_holding_registers,
            "holding_registers_ror" : self.read_multi_holding_registers,
            "data_registers" : self.read_multi_holding_registers,
            "timers" : self.read_multi_holding_registers,
            "counters" : self.read_multi_holding_registers,
            "counters_32bit" : self.read_counters_32bit,
         }

    def read(self, fatek_addresses: list, *args, **kwargs) -> dict():

        fatek_by_type = FatekByType(fatek_addresses)

        result = {}

        for type, values in fatek_by_type.data.items():
            read_function = self.type_to_function[type]
            result = result | self._read_main(values, read_function, True, *args, **kwargs)
        
        return result

    def read_counters_32bit(self, counters_32bit: FatekList, return_dict: bool = False):
        pass

    def _read_main(self, fatek_addresses: FatekList, function, return_dict: bool = False, read_mask: int = 1):
        
        modbus_numbers = fatek_addresses.modbus_numbers
        fatek_addresses_in_str = fatek_addresses.addresses
        type_size = fatek_addresses.type_size

        read_mask = type_size if type_size else read_mask

        self.open()
        modbus_values = function(modbus_numbers, read_mask=read_mask)

        if return_dict:
            dict_to_return =  dict(zip(fatek_addresses_in_str, modbus_values))
            return dict_to_return
        return modbus_values





