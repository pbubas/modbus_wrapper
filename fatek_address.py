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

    @property
    def discret_inputs(self):
        fatek_list = self.fatek_list
        return [entry.address for entry in fatek_list if entry.type == "discret_inputs"]
    
    @property
    def discret_outputs(self):
        fatek_list = self.fatek_list
        return [entry.address for entry in fatek_list if entry.type == "discret_outputs"]
    
    @property
    def holding_registers(self):
        fatek_list = self.fatek_list
        return [entry.address for entry in fatek_list if entry.type == "holding_registers"]
        
        
    @staticmethod
    def convert_range(read_range: str):
        read_range = read_range.split("-")
        start_address = read_range[0]
        end_address = read_range[1]





    


        