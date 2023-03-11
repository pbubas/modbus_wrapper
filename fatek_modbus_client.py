import logging
from modbus_client_wrapper import ModbusClientWrapper
from fatek_address import FatekAddress

LOG = logging.getLogger(__name__)

class FatekAddressValidationError(Exception):
    pass

class FatekModbusClient:

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        self.client = ModbusClientWrapper(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)

    def read(self, fatek_addresses: list) -> dict():
        """ 
        TIMERS_DATA, COUNTERS_DATA, COUNTERS_32BIT can be read by individual functions due to name conflict:
            TIMERS_DATA -> read_timers_data()
            COUNTERS_DATA -> read_counters_data()
            COUNTERS_32BIT -> read_counters_32bit()
        """
        
        discrete_inputs = list()
        discrete_outputs = list()
        discrete_mrelays = list()
        discrete_srelays = list()
        timers = list()
        counters = list()
        holding_registers = list()
        holding_registers_ror = list()
        data_registers = list()


        for address in fatek_addresses:
            if address in FatekAddress.DISCRET_INPUTS.keys():
                discrete_inputs.append(address)

            elif address in FatekAddress.DISCRET_OUTPUTS.keys():
                discrete_outputs.append(address)

            elif address in FatekAddress.DISCRET_MRELAYS.keys():
                discrete_mrelays.append(address)

            elif address in FatekAddress.DISCRET_SRELAYS.keys():
                discrete_srelays.append(address)
            
            elif address in FatekAddress.TIMERS_STATUS.keys():
                timers.append(address)

            elif address in FatekAddress.COUNTERS_STATUS.keys():
                counters.append(address)

            elif address in FatekAddress.HOLDING_REGISTERS.keys():
                holding_registers.append(address)

            elif address in FatekAddress.HOLDING_REGISTERS_ROR.keys():
                holding_registers_ror.append(address)

            elif address in FatekAddress.DATA_REGISTERS.keys():
                data_registers.append(address)
            
            else:
                raise FatekAddressValidationError(f'address {address} not recgnized as Fatek address')

        result = {}
        
        if discrete_inputs:
            result = result | self.read_discrete_inputs(discrete_inputs, True)

        if discrete_outputs:
            result = result | self.read_discrete_outputs(discrete_outputs, True)

        if discrete_mrelays:
            result = result | self.read_discrete_mrelays(discrete_mrelays, True)

        if discrete_srelays:
            result = result | self.read_discrete_srelays(discrete_srelays, True)

        if timers:
            result = result | self.read_timers_status(timers, True)

        if counters:
            result = result | self.read_counter_status(counters, True)

        if holding_registers:
            result = result | self.read_holding_registers(holding_registers, True)

        if holding_registers_ror:
            result = result | self.read_holding_registers_ror(holding_registers_ror, True)

        if data_registers:
            result = result | self.read_data_registers(data_registers, True)

        return result

    def read_discrete_inputs(self, discrete_inputs: list, return_dict: bool = False):

        return self._read_main(
            discrete_inputs, 
            self.client.read_multi_coils, 
            FatekAddress.DISCRET_INPUTS, 
            return_dict
            )

    def read_discrete_outputs(self, discrete_outputs: list, return_dict: bool = False):
        return self._read_main(
            discrete_outputs, 
            self.client.read_multi_coils, 
            FatekAddress.DISCRET_OUTPUTS, 
            return_dict
            )

    def read_discrete_mrelays(self, discrete_mrelays: list, return_dict: bool = False):
        return self._read_main(
            discrete_mrelays, 
            self.client.read_multi_coils, 
            FatekAddress.DISCRET_MRELAYS, 
            return_dict
            )

    def read_discrete_srelays(self, discrete_srelays: list, return_dict: bool = False):
        return self._read_main(
            discrete_srelays, 
            self.client.read_multi_coils, 
            FatekAddress.DISCRET_SRELAYS, 
            return_dict
            )

    def read_timers_status(self, timers: list, return_dict: bool = False):
        return self._read_main(
            timers, 
            self.client.read_multi_coils, 
            FatekAddress.TIMERS_STATUS, 
            return_dict
            )

    def read_counter_status(self, counters: list, return_dict: bool = False):
        return self._read_main(
            counters, 
            self.client.read_multi_coils, 
            FatekAddress.COUNTERS_STATUS, 
            return_dict
            )

    def read_holding_registers(self, holding_registers: list, return_dict: bool = False):
        return self._read_main(
            holding_registers, 
            self.client.read_multi_holding_registers, 
            FatekAddress.HOLDING_REGISTERS, 
            return_dict
            )

    def read_holding_registers_ror(self, holding_registers_ror: list, return_dict: bool = False):
        return self._read_main(
            holding_registers_ror, 
            self.client.read_multi_holding_registers, 
            FatekAddress.HOLDING_REGISTERS_ROR, 
            return_dict
            )

    def read_data_registers(self, data_registers: list, return_dict: bool = False):
        return self._read_main(
            data_registers,
            self.client.read_multi_holding_registers, 
            FatekAddress.DATA_REGISTERS, 
            return_dict
            )

    def read_timers_data(self, timers: list, return_dict: bool = False):
        return self._read_main(
            timers,
            self.client.read_multi_holding_registers, 
            FatekAddress.TIMERS_DATA, 
            return_dict
            )

    def read_counters_data(self, counters: list, return_dict: bool = False):
        return self._read_main(
            counters,
            self.client.read_multi_holding_registers, 
            FatekAddress.COUNTERS_DATA, 
            return_dict
            )

    def read_counters_32bit(self, counters_32bit: list, return_dict: bool = False):
        pass

    def _read_main(self, fatek_addresses: list(), function, fatek_type: dict(), return_dict: bool = False):
        try:
            modbus_numbers = [fatek_type[address] for address in fatek_addresses]
        except KeyError as e:
            error_message = f'address {str(e)} not recgnized as Fatek address'
            raise FatekAddressValidationError(error_message)

        read_mask = len(fatek_type.keys())

        self.client.open()
        modbus_values = function(modbus_numbers, read_mask=read_mask)

        if return_dict:
            dict_to_return =  dict(zip(fatek_addresses, modbus_values))
            return dict_to_return
        return modbus_values





