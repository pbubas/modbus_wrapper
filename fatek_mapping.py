from modbus_functions_map import (
        READ_COILS,
        READ_HOLDING_REGISTERS,
        WRITE_SINGLE_COIL,
        WRITE_SINGLE_HOLDING_REGISTER,
        WRITE_MULTIPLE_COILS,
        WRITE_MULTIPLE_HOLDING_REGISTERS,
)
from dataclasses import dataclass

__doc__ = """
## 1-bit coils
#### Discrete outputs: Y0 - Y255
#### Discrete inputs: X0 - X255
#### Discrete relays M: M0 - M2001
#### Discrete relays S: S0 - S999
#### Timers status: T0 - T255
#### Counters status: C0 - C255
## 16-bit registers
#### Holding registers: R0 - R4167
#### Holding registers ror: R5000 - R5998
#### Data registers ror: D0 - D2998
#### Timers data ror: T0 - T255
#### Counters data: C0 - C199
## 32-bit registers
#### Counters data: C200 - C255
"""

FATEK_TO_MODBUS_MAP = {
    # 1-bit coils
    "discret_srelays" : {"S"+str(fatek_address):fatek_address+6001 for fatek_address in range(0,1000)},
    "discret_mrelays" : {"M"+str(fatek_address):fatek_address+2001 for fatek_address in range(0,2002)},
    "discret_inputs" : {"X"+str(fatek_address):fatek_address+1001 for fatek_address in range(0,256)},
    "discret_outputs" : {"Y"+str(fatek_address):fatek_address+1 for fatek_address in range(0,256)},
    "timers_status" : {"T"+str(fatek_address):fatek_address+9001 for fatek_address in range(0,256)},
    "counters_status" : {"C"+str(fatek_address):fatek_address+9501 for fatek_address in range(0,256)},
    # 16-bit registers
    "holding_registers" : {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(0,4168)},
    "holding_registers_ror" : {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(5000,5998)},
    "data_registers" : {"D"+str(fatek_address):fatek_address+406001 for fatek_address in range(0,2999)},
    "timers" : {"RT"+str(fatek_address):fatek_address+409001 for fatek_address in range(0,256)},
    "counters" : {"RC"+str(fatek_address):fatek_address+409501 for fatek_address in range(0,200)},
    # 32-bit registers
    "counters_32bit" : {
        "C"+str(fatek_address):modbus_address for fatek_address, modbus_address in 
        list(zip(range(200,256), range(49701,49812,2)))
        }
}

@dataclass
class FatekType:
    name: str
    read_function: int
    write_function: int = None
    multi_write_function: int = None

    def __post_init__(self):
        self.address_map = FATEK_TO_MODBUS_MAP[self.name]
        self.type_size = len(FATEK_TO_MODBUS_MAP[self.name].values())


FATEK_TYPES = [
        FatekType(
                'holding_registers',
                READ_HOLDING_REGISTERS,
                WRITE_SINGLE_HOLDING_REGISTER,
                WRITE_MULTIPLE_HOLDING_REGISTERS,
        ),

        FatekType(
                "discret_mrelays",
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),

        FatekType(
                'discret_inputs',
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),

        FatekType(
                'discret_outputs',
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),

         FatekType(
                'data_registers',
                READ_HOLDING_REGISTERS,
                WRITE_SINGLE_HOLDING_REGISTER,
                WRITE_MULTIPLE_HOLDING_REGISTERS,
        ),

        FatekType(
                'holding_registers_ror',
                READ_HOLDING_REGISTERS,
                WRITE_SINGLE_HOLDING_REGISTER,
                WRITE_MULTIPLE_HOLDING_REGISTERS,
        ),

        FatekType(
                'counters',
                READ_HOLDING_REGISTERS,
                WRITE_SINGLE_HOLDING_REGISTER,
                WRITE_MULTIPLE_HOLDING_REGISTERS,
        ),

        FatekType(
                'timers',
                READ_HOLDING_REGISTERS,
                WRITE_SINGLE_HOLDING_REGISTER,
                WRITE_MULTIPLE_HOLDING_REGISTERS,
        ),

        FatekType(
                "discret_srelays",
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),


        FatekType(
                "timers_status",
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),

        FatekType(
                "counters_status",
                READ_COILS,
                WRITE_SINGLE_COIL,
                WRITE_MULTIPLE_COILS,
        ),
]
