from .base import ModbusBaseClientWrapper
from pymodbus.client import ModbusSerialClient, ModbusTcpClient, ModbusUdpClient
from .. import modbus_function_code 



class ModbusTcpClientWrapper(ModbusTcpClient, ModbusBaseClientWrapper):

    def __init__(self, host='localhost', port=502, *args, **kwargs):
        ModbusTcpClient.__init__(self, host=host, port=port, *args, **kwargs)
        ModbusBaseClientWrapper.__init__(self)


class ModbusUdpClientWrapper(ModbusUdpClient, ModbusBaseClientWrapper):
    def __init__(self, host='localhost', port=502, *args, **kwargs):
        ModbusUdpClient.__init__(self, host=host, port=port, *args, **kwargs)
        ModbusBaseClientWrapper.__init__(self)


class ModbusSerialClientWrapper(ModbusSerialClient, ModbusBaseClientWrapper):
    def __init__(
        self, 
        port,
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=1,
        *args, 
        **kwargs
                 ):
    
        ModbusSerialClient.__init__(
                self,
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                timeout=timeout,
                *args, 
                **kwargs
                )        
      
        ModbusBaseClientWrapper.__init__(self)
