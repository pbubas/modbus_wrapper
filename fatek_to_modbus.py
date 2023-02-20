
class FatekToModbus:
    """
        # 1-bit coils


    """
    # 1-bit coils
    DISCRET_SRELAYS = {"S"+str(fatek_address):fatek_address+6001 for fatek_address in range(0,1000)}
    DISCRET_MRELAYS = {"M"+str(fatek_address):fatek_address+2001 for fatek_address in range(0,2002)}
    DISCRET_INPUTS = {"X"+str(fatek_address):fatek_address+1001 for fatek_address in range(0,256)}
    DISCRET_OUTPUTS = {"Y"+str(fatek_address):fatek_address+1 for fatek_address in range(0,256)}
    TIMERS_STATUS = {"T"+str(fatek_address):fatek_address+9001 for fatek_address in range(0,256)}
    COUNTERS_STATUS = {"C"+str(fatek_address):fatek_address+9501 for fatek_address in range(0,256)}
    # 16-bit registers
    HOLDING_REGISTERS = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(0,4168)}
    HOLDING_REGISTERS_ROR = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(5000,5998)}
    DATA_REGISTERS = {"D"+str(fatek_address):fatek_address+406001 for fatek_address in range(0,2999)}
    TIMERS_DATA = {"T"+str(fatek_address):fatek_address+409001 for fatek_address in range(0,256)}
    COUNTERS_DATA = {"C"+str(fatek_address):fatek_address+409501 for fatek_address in range(0,200)}
    # 32-bit registers
    COUNTERS_32BIT = {
        "C"+str(fatek_address):modbus_address for fatek_address, modbus_address in 
        list(zip(range(200,256), range(49701,49812,2)))
        }

    COILS = (
            DISCRET_INPUTS | DISCRET_OUTPUTS | DISCRET_SRELAYS | 
            DISCRET_MRELAYS | TIMERS_STATUS | COUNTERS_STATUS
        )

    REG_16BIT = (
        HOLDING_REGISTERS | HOLDING_REGISTERS_ROR | DATA_REGISTERS |
        TIMERS_DATA| COUNTERS_DATA
        )

    REG_32BIT = (
            COUNTERS_32BIT
        )
    


        