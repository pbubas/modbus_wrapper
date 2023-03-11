import fatek_mapping 
from typing import List


class FatekAddress:
    
    def __init__(self, fatek_address: str):
        fatek_addresses = fatek_mapping.ALL.keys()
        doc = fatek_mapping.__doc__

        if fatek_address in fatek_addresses:
            self.address = fatek_address 
        else:
            raise Exception(f'address "{fatek_address}" not recognized, provide correct address: {doc}')


    @property
    def modbus_number(self):
        address = self.address
        all_modbus_numbers = fatek_mapping.ALL

        try:
            modbus_number = all_modbus_numbers[address]
        except KeyError:
            raise Exception(f"could not find Modbus number for address {address}")
        
        return modbus_number
    
    def _get_modbus_function_code(self):
        pass
    
    @property
    def type(self):
        address = self.address
        modbus_map = fatek_mapping.MAP

        return next(
            address_type for address_type, values in modbus_map.items() if address in values.keys()
            )


class FatekList(list):

    def __init__ (self, fatek_list: List[FatekAddress]):
        super().__init__(fatek_list)

    @property
    def modbus_numbers(self):
        return [i.modbus_number for i in self]
    
    @property
    def addresses(self):
        return [i.address for i in self]
    
    @property
    def type_size(self):
        all_types = {i.type for i in self}
        if len(all_types) == 1:
            type = next(i for i in all_types)
            return len(fatek_mapping.MAP[type])
    

class FatekByType(list):
    def __init__ (self, fatek_list: list):

        _fatek_list = []
        for entry in fatek_list:
            if "-" in entry:
                _fatek_list = _fatek_list + (self.convert_range(entry))
            else:
                _fatek_list.append(entry)

        fatek_list = [FatekAddress(entry) for entry in _fatek_list]

        super().__init__(fatek_list)

        all_types = {entry.type for entry in self}
        
        for type in all_types:
            self.__dict__[type] = self._get_types(type)
            
    def _get_types(self, fatek_type: str):
        return FatekList([entry for entry in self if entry.type == fatek_type])
    
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




    


        