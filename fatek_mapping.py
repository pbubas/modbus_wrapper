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
MAP = {
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

COILS = (
        MAP["discret_inputs"] | MAP["discret_outputs"] | 
        MAP["discret_srelays"] | MAP["discret_mrelays"] |
        MAP["timers_status"] | MAP["counters_status"]
    )

REG_16BIT = (
    MAP["holding_registers"] | MAP["holding_registers_ror"] |
    MAP["data_registers"] |
    MAP["timers"] | MAP["counters"]
    )

REG_32BIT = (
        MAP["counters_32bit"]
    )


ALL = COILS | REG_16BIT | REG_32BIT

READ_COILS = 0x01
READ_MULTIPLE_HOLDING_REGISTERS = 0x03

MODBUS_READ_FUNCTION_CODES = {
        "discret_srelays": READ_COILS,
        "discret_mrelays": READ_COILS,
        "discret_inputs" : READ_COILS,
        "discret_outputs" : READ_COILS,
        "timers_status" : READ_COILS,
        "counters_status" : READ_COILS,
        "holding_registers" : READ_MULTIPLE_HOLDING_REGISTERS,
        "holding_registers_ror" : READ_MULTIPLE_HOLDING_REGISTERS,
        "data_registers" : READ_MULTIPLE_HOLDING_REGISTERS,
        "timers" : READ_MULTIPLE_HOLDING_REGISTERS,
        "counters" : READ_MULTIPLE_HOLDING_REGISTERS,
        "counters_32bit" : READ_MULTIPLE_HOLDING_REGISTERS,
}

WRITE_SINGLE_COIL = 0x05
WRITE_SINGLE_HOLDING_REGISTER = 0x06

MODBUS_WRITE_FUNCTION_CODES = {
        "discret_srelays": WRITE_SINGLE_COIL,
        "discret_mrelays": WRITE_SINGLE_COIL,
        "discret_inputs" : WRITE_SINGLE_COIL,
        "discret_outputs" : WRITE_SINGLE_COIL,
        "timers_status" : WRITE_SINGLE_COIL,
        "counters_status" : WRITE_SINGLE_COIL,
        "holding_registers" : WRITE_SINGLE_HOLDING_REGISTER,
        "holding_registers_ror" : WRITE_SINGLE_HOLDING_REGISTER,
        "data_registers" : WRITE_SINGLE_HOLDING_REGISTER,
        "timers" : WRITE_SINGLE_HOLDING_REGISTER,
        "counters" : WRITE_SINGLE_HOLDING_REGISTER,
        "counters_32bit" : WRITE_SINGLE_HOLDING_REGISTER,
}

WRITE_MULTIPLE_COILS = 0x15
WRITE_MULTIPLE_HOLDING_REGISTERS = 0x16

MODBUS_MULTI_WRITE_FUNCTION_CODES = {
        "discret_srelays": WRITE_MULTIPLE_COILS,
        "discret_mrelays": WRITE_MULTIPLE_COILS,
        "discret_inputs" : WRITE_MULTIPLE_COILS,
        "discret_outputs" : WRITE_MULTIPLE_COILS,
        "timers_status" : WRITE_MULTIPLE_COILS,
        "counters_status" : WRITE_MULTIPLE_COILS,
        "holding_registers" : WRITE_MULTIPLE_HOLDING_REGISTERS,
        "holding_registers_ror" : WRITE_MULTIPLE_HOLDING_REGISTERS,
        "data_registers" : WRITE_MULTIPLE_HOLDING_REGISTERS,
        "timers" : WRITE_MULTIPLE_HOLDING_REGISTERS,
        "counters" : WRITE_MULTIPLE_HOLDING_REGISTERS,
        "counters_32bit" : WRITE_MULTIPLE_HOLDING_REGISTERS,
}