import fatek_mapping 

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

    

class FatekList(tuple):

    def __new__ (cls, fatek_list: tuple):
        fatek_list = (FatekAddress(entry) for entry in fatek_list)
        return super().__new__(cls, fatek_list)

    def _get_types(self, fatek_type: str):
        return tuple(entry for entry in self if entry.type == fatek_type)

    @property
    def discret_inputs(self):
        return self._get_types("discret_inputs")
    
    @property
    def discret_outputs(self):
        return self._get_types("discret_outputs")
    
    @property
    def holding_registers(self):
        return self._get_types("holding_registers")
        
        
    @staticmethod
    def convert_range(fatek_range: str):

        fatek_range = fatek_range.split("-")

        address_prefix = fatek_range[0][:1]
        start_address = int(fatek_range[0][1:])
        end_address = int(fatek_range[1]) + 1

        address_range = list(range(start_address, end_address))

        return [address_prefix + str(address) for address in address_range]





    


        