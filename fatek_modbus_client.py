import logging
from modbus_client_wrapper import ModbusClientWrapper
from fatek_address import FatekByType, FatekList
from typing import Union, List
from write_model import WriteModel

LOG = logging.getLogger(__name__)


class FatekModbusClient(ModbusClientWrapper):

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.function_map = {
            0x01: self.read_multi_coils,
            0x03: self.read_multi_holding_registers,
            0x05: self.write_single_coil,
            0x06: self.write_single_register,
            0x15: self.write_multiple_coils,
            0x16: self.write_multiple_registers
         }

    def read(self, fatek_addresses: list, *args, **kwargs) -> dict():

        fatek_by_type = FatekByType(fatek_addresses)

        result = {}

        for values in fatek_by_type.data.values():
            read_function = self.function_map[values.modbus_read_function_code]
            result = result | self._read_main(values, read_function, True, *args, **kwargs)
        
        return result

    def read_counters_32bit(self, counters_32bit: FatekList, return_dict: bool = False):
        pass

    def write_counters_32bit(self, counters_32bit: FatekList, return_dict: bool = False):
        pass
    
    def write(self, fatek_address: str, value: Union[bool, int, List[bool], List[int]]):
        write_model = WriteModel(fatek_address=fatek_address, value=value)
        fatek_address = write_model.fatek_address
        value = write_model.value
        modbus_address = fatek_address.modbus_address

        if isinstance(value, list):
            function = self.function_map[fatek_address.modbus_multi_write_function_code]
        else:
            function = self.function_map[fatek_address.modbus_write_function_code]

        self.open()
        return function(modbus_address, value)


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





