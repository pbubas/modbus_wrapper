import fatek_mapping
from typing import List, Union
from modbus_client_wrapper import ModbusClientWrapper


class FatekAddressValidationException(Exception):
    pass


class FatekListValidationException(Exception):
    pass


class FatekAddress:
    
    def __init__(self, fatek_address: str):
        doc = fatek_mapping.__doc__

        try:
            fatek_type = next(fatek_type 
                for fatek_type in fatek_mapping.FATEK_TYPES 
                if fatek_address in fatek_type.address_map.keys())
        except StopIteration:
            raise FatekAddressValidationException(f'address "{fatek_address}" not recognized, provide correct address: {doc}')
        else:
            self.fatek_address = fatek_address
            self.modbus_number =  fatek_type.address_map[fatek_address]
            self.modbus_address = ModbusClientWrapper.get_address(self.modbus_number)
            self.modbus_read_function_code = fatek_type.read_function
            self.modbus_write_function_code = fatek_type.write_function
            self.modbus_multi_write_function_code = fatek_type.multi_write_function
            self.name = fatek_type.name
            self.type_size = fatek_type.type_size


class FatekList(list):

    def __init__ (self, fatek_list: List[FatekAddress]):
        super().__init__(fatek_list)

        all_types = {i.name for i in self}
        if len(all_types) != 1: 
            raise FatekListValidationException(f"fatek addresse needs to be same type")
        
        self.name = self[0].name
        self.type_size = self[0].type_size
        self.modbus_read_function_code = self[0].modbus_read_function_code
        self.modbus_write_function_code = self[0].modbus_write_function_code
        self.modbus_multi_write_function_code = self[0].modbus_multi_write_function_code


    @property
    def modbus_numbers(self):
        return [i.modbus_number for i in self]
    
    @property
    def addresses(self):
        return [i.fatek_address for i in self]
    

class FatekByType(list):
    def __init__ (self, fatek_list: Union[list,str]):
        if not isinstance(fatek_list, list):
            fatek_list = list([fatek_list])

        _fatek_list = []
        for entry in fatek_list:
            if "-" in entry:
                _fatek_list = _fatek_list + (self.convert_range(entry))
            else:
                _fatek_list.append(entry)

        fatek_list = [FatekAddress(entry) for entry in _fatek_list]

        super().__init__(fatek_list)

        all_types = {entry.name for entry in self}
        
        for type in all_types:
            self.__dict__[type] = self._get_types(type)
            
    def _get_types(self, fatek_type: str):
        return FatekList([entry for entry in self if entry.name == fatek_type])
    
    @property
    def data(self):
        return self.__dict__
    
    def convert_range(self, fatek_range: str):

        fatek_range = fatek_range.split("-")

        address_prefix = fatek_range[0][:1]
        start_address = int(fatek_range[0][1:])
        end_address = int(fatek_range[1]) + 1

        address_range = list(range(start_address, end_address))

        return [address_prefix + str(address) for address in address_range]
    





    


        