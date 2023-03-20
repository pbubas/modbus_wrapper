from dataclasses import dataclass

class ModbusValueException(Exception):
    pass

@dataclass
class IntValue:
    """16bit integer for modbus registers"""

    unsign_int: int #0 to 65535
    sign_int: int #-32768 to 32767

    @classmethod
    def from_sign_int(cls, sign_int: int | None):
        if sign_int == None:
            return None

        valid_int = lambda x:  type(x) == int
        valid_sign_range = lambda x: -32768 <= x <= 32767

        valid16bit_sign_int = lambda x: all(
                    [valid_int(x), valid_sign_range(x)]
                )

        if not valid16bit_sign_int(sign_int): 
            raise ModbusValueException(f'value {sign_int} invalid')

        unsign_int =  sign_int & 0xffff
        return cls(unsign_int, sign_int)

    @classmethod
    def from_unsign_int(cls, unsign_int: int | None):
        if unsign_int == None:
            return None

        valid_int = lambda x:  type(x) == int
        valid_unsign_range = lambda x: 0 <= x <= 0xffff
        
        valid16bit_unsign_int = lambda x: all(
                    [valid_int(x), valid_unsign_range(x)]
                )
            
        if not valid16bit_unsign_int(unsign_int): 
            raise ModbusValueException(f'value {unsign_int} invalid')

        sign_int =  -(2**16 - unsign_int) if unsign_int < 0 else unsign_int
        return cls(unsign_int, sign_int)

    def __repr__(self):
        return str(self.sign_int)

    def __eq__(self, value):
        return self.unsign_int == value

class BoolValue:
    def __new__(cls, value: bool | int | None):
        if value == None:
            return None

        if type(value) == bool or value in [0,1]:
            return bool(value)
        raise ModbusValueException(f'value "{value}" is not correct bool')
    
