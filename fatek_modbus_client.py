from modbus_client_wrapper import ModbusClientWrapper
from fatek_to_modbus import FatekToModbus



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

        discrete_inputs = [address for address in fatek_addresses if address in FatekToModbus.DISCRET_INPUTS.keys()]
        discrete_outputs = [address for address in fatek_addresses if address in FatekToModbus.DISCRET_OUTPUTS.keys()]
        discrete_mrelays = [address for address in fatek_addresses if address in FatekToModbus.DISCRET_MRELAYS.keys()]
        discrete_srelays = [address for address in fatek_addresses if address in FatekToModbus.DISCRET_SRELAYS.keys()]
        timers = [address for address in fatek_addresses if address in FatekToModbus.TIMERS_STATUS.keys()]
        counters = [address for address in fatek_addresses if address in FatekToModbus.COUNTERS_STATUS.keys()]

        holding_registers = [address for address in fatek_addresses if address in FatekToModbus.HOLDING_REGISTERS.keys()]
        holding_registers_ror = [address for address in fatek_addresses if address in FatekToModbus.HOLDING_REGISTERS_ROR.keys()]
        data_registers = [address for address in fatek_addresses if address in FatekToModbus.DATA_REGISTERS.keys()]

        return (
            self.read_discrete_inputs(discrete_inputs, True) |
            self.read_discrete_outputs(discrete_outputs, True) |
            self.read_discrete_mrelays(discrete_mrelays, True) |
            self.read_discrete_srelays(discrete_srelays, True) |
            self.read_timers_status(timers, True) |
            self.read_counter_status(counters, True) |
            self.read_holding_registers(holding_registers, True) |
            self.read_holding_registers_ror(holding_registers_ror, True) |
            self.read_data_registers(data_registers, True)
        )

    def read_discrete_inputs(self, discrete_inputs: list, return_dict: bool = False):

        return self._read_main(
            discrete_inputs, 
            self.client.read_multi_coils, 
            FatekToModbus.DISCRET_INPUTS, 
            True
            )

    def read_discrete_outputs(self, discrete_outputs: list, return_dict: bool = False):
        return self._read_main(
            discrete_outputs, 
            self.client.read_multi_coils, 
            FatekToModbus.DISCRET_OUTPUTS, 
            True
            )

    def read_discrete_mrelays(self, discrete_mrelays: list, return_dict: bool = False):
        return self._read_main(
            discrete_mrelays, 
            self.client.read_multi_coils, 
            FatekToModbus.DISCRET_MRELAYS, 
            True
            )

    def read_discrete_srelays(self, discrete_srelays: list, return_dict: bool = False):
        return self._read_main(
            discrete_srelays, 
            self.client.read_multi_coils, 
            FatekToModbus.DISCRET_SRELAYS, 
            True
            )

    def read_timers_status(self, timers: list, return_dict: bool = False):
        return self._read_main(
            timers, 
            self.client.read_multi_coils, 
            FatekToModbus.TIMERS_STATUS, 
            True
            )

    def read_counter_status(self, counters: list, return_dict: bool = False):
        return self._read_main(
            counters, 
            self.client.read_multi_coils, 
            FatekToModbus.COUNTERS_STATUS, 
            True
            )

    def read_holding_registers(self, holding_registers: list, return_dict: bool = False):
        return self._read_main(
            holding_registers, 
            self.client.read_multi_holding_registers, 
            FatekToModbus.HOLDING_REGISTERS, 
            True
            )

    def read_holding_registers_ror(self, holding_registers_ror: list, return_dict: bool = False):
        return self._read_main(
            holding_registers_ror, 
            self.client.read_multi_holding_registers, 
            FatekToModbus.HOLDING_REGISTERS_ROR, 
            True
            )

    def read_data_registers(self, data_registers: list, return_dict: bool = False):
        return self._read_main(
            data_registers,
            self.client.read_multi_holding_registers, 
            FatekToModbus.DATA_REGISTERS, 
            True
            )

    def read_timers_data(self, timers: list, return_dict: bool = False):
        return self._read_main(
            timers,
            self.client.read_multi_holding_registers, 
            FatekToModbus.TIMERS_DATA, 
            True
            )

    def read_counters_data(self, counters: list, return_dict: bool = False):
        return self._read_main(
            counters,
            self.client.read_multi_holding_registers, 
            FatekToModbus.COUNTERS_DATA, 
            True
            )

    def read_counters_32bit(self, counters_32bit: list, return_dict: bool = False):
        pass

    def _read_main(self, fatek_addresses: list(), function, fatek_type: dict(), return_dict: bool = False):
        modbus_numbers = [fatek_type[address] for address in fatek_addresses]

        read_mask = len(fatek_type.keys())
        modbus_values = function(modbus_numbers, read_mask=read_mask)

        if return_dict:
            dict_to_return =  dict(zip(fatek_addresses, modbus_values))
            return dict_to_return
        return modbus_values
