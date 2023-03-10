from fatek_mapping import MAP, ALL


class FatekAddress:
    


    def __init__(self, fatek_address: str):
        self.address = fatek_address


    @property
    def modbus_number(self):
        address = self.address
        all_modbus_numbers = ALL

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

        for key, value in MAP.items():

            if address in value.keys(): 
                address_type = key
                break

        return address_type
    

class FatekList:

    def __init__(self, fatek_list: list):
        self.fatek_list = [FatekAddress(entry) for entry in fatek_list]

    def _get_types(self, fatek_type: str):
        fatek_list = self.fatek_list
        return [entry for entry in fatek_list if entry.type == fatek_type]

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





    


        