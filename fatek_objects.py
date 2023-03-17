from modbus_objects import (
    Coil as ModbusCoil,
    HoldingRegister as ModbusHoldingRegister
)
from typing import Union

class FatekObject:
    """Basic Fatek Object"""

    def __init__(self, fatek_number: str, value_to_write: Union[int, bool] = None):
        self.fatek_number = fatek_number
        modbus_number = self.FATEK_MAP[self.fatek_number]
        super().__init__(modbus_number, value_to_write)

    def __repr__(self):
        return str(self.fatek_number)


class DiscretMrelay(FatekObject, ModbusCoil):
    FATEK_MAP = {"M"+str(fatek_address):fatek_address+2001 for fatek_address in range(0,2002)}
    VALUES = FATEK_MAP.keys()


class DiscretSrelay(FatekObject, ModbusCoil):
    FATEK_MAP = {"S"+str(fatek_address):fatek_address+6001 for fatek_address in range(0,1000)}
    VALUES = FATEK_MAP.keys()


class DiscretInput(FatekObject, ModbusCoil):
    FATEK_MAP = {"X"+str(fatek_address):fatek_address+1001 for fatek_address in range(0,256)}
    VALUES = FATEK_MAP.keys()


class DiscretOuput(FatekObject, ModbusCoil):
    FATEK_MAP = {"Y"+str(fatek_address):fatek_address+1 for fatek_address in range(0,256)}
    VALUES = FATEK_MAP.keys()


class TimerStatus(FatekObject, ModbusCoil):
    FATEK_MAP = {"T"+str(fatek_address):fatek_address+9001 for fatek_address in range(0,256)}
    VALUES = FATEK_MAP.keys()


class CounterStatus(FatekObject, ModbusCoil):
    FATEK_MAP = {"C"+str(fatek_address):fatek_address+9501 for fatek_address in range(0,256)}
    VALUES = FATEK_MAP.keys()


class HoldingRegister(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(0,4168)}
    VALUES = FATEK_MAP.keys()


class HoldingRegisterRor(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(5000,5998)}
    VALUES = FATEK_MAP.keys()


class DataRegister(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {"D"+str(fatek_address):fatek_address+406001 for fatek_address in range(0,2999)}
    VALUES = FATEK_MAP.keys()


class Timer(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {"RT"+str(fatek_address):fatek_address+409001 for fatek_address in range(0,256)}
    VALUES = FATEK_MAP.keys()


class Counter(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {"RC"+str(fatek_address):fatek_address+409501 for fatek_address in range(0,200)}
    VALUES = FATEK_MAP.keys()


class Counter32(FatekObject, ModbusHoldingRegister):
    FATEK_MAP = {
        "C"+str(fatek_address):modbus_address for fatek_address, modbus_address in 
        list(zip(range(200,256), range(49701,49812,2)))
        }
    VALUES = FATEK_MAP.keys()
