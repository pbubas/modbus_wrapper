
class Fatek2Modbus:
    # 1-bit coils
    _discreet_srelay_map = {"S"+str(fatek_address):fatek_address+6001 for fatek_address in range(0,1000)}
    _discreet_mrelay_map = {"M"+str(fatek_address):fatek_address+2001 for fatek_address in range(0,2002)}
    _discreet_input_map = {"X"+str(fatek_address):fatek_address+1001 for fatek_address in range(0,256)}
    _discreet_ouptut_map = {"Y"+str(fatek_address):fatek_address+1 for fatek_address in range(0,256)}
    _timer_status_map = {"T"+str(fatek_address):fatek_address+9001 for fatek_address in range(0,256)}
    _counter_status_map = {"C"+str(fatek_address):fatek_address+9501 for fatek_address in range(0,256)}
    # 16-bit registers
    _register_map = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(0,4168)}
    _register_ror_map = {"R"+str(fatek_address):fatek_address+400001 for fatek_address in range(5000,5998)}
    _register_data_map = {"D"+str(fatek_address):fatek_address+406001 for fatek_address in range(0,2999)}
    _timer_data_map = {"T"+str(fatek_address):fatek_address+409001 for fatek_address in range(0,256)}
    _counter_data_map = {"C"+str(fatek_address):fatek_address+409501 for fatek_address in range(0,200)}
    # 32-bit registers
    _counter32_data_map = {
        "C"+str(fatek_address):modbus_address for fatek_address, modbus_address in 
        list(zip(range(200,256), range(49701,49812,2)))
        }

    COILS = (
            _discreet_mrelay_map | _discreet_srelay_map | _discreet_input_map | 
            _discreet_ouptut_map | _timer_status_map | _counter_status_map
        )

    REG_16BIT = (
        _register_map | _register_ror_map | _register_data_map |
        _timer_data_map| _counter_data_map
        )

    REG_32BIT = (
            _counter32_data_map
        )