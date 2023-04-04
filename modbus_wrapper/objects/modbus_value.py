from dataclasses import dataclass
from abc import ABC, abstractmethod

class ModbusValueException(Exception):
    pass

class BaseValue(ABC):
    """Base Value class for modbus objects"""

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    def __eq__(self, value):
        return self.value == value

    def __bool__(self):
        return False if self.value is None else True

    def update(self, new_value: int | bool | None):
        """method to update collected value, None values are ignored"""
        if new_value == None:
            self.changed = False
            self.value = None
            return None
        
        self.validate(new_value)

        previous_value = self.value

        value_changed = all([previous_value != new_value, previous_value != None])
        value_unchanged = all([previous_value == new_value, previous_value != None])

        if value_changed:
            self.changed = True
        elif value_unchanged:
            self.changed = False

        self.value = new_value
        return self.value

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, change_bit: bool):
        self._changed = change_bit


class RegisterValue(BaseValue):
    """16bit integer for modbus registers"""

    def __init__(self, unsign_int: int = None):

        self.validate(unsign_int)
        self.value = unsign_int
        self._changed: bool = None

    def __repr__(self):
        return str(self.signed)

    def validate(self, unsign_int):
        if unsign_int is None:
            return True

        unsign_int.to_bytes(2, "big")
        return True

    @property
    def _in_bytes(self):
        if self.value: 
            in_bytes = self.value.to_bytes(2, "big")
            return in_bytes

    @property
    def signed(self):
        if self.value is None: return None
        if self.value == 0: return 0
        signed = int.from_bytes(self._in_bytes, "big", signed=True)
        return signed
    

class CoilValue(BaseValue):

    def __init__(self, value: bool = None):
        self.validate(value)
        self.value = value
        self._changed: bool = None

    def validate(self, value: bool | int | None):
        if value is None:
            return True

        if type(value) == bool or value in [0,1]:
            return True
        raise ModbusValueException(f'value "{value}" is not correct bool')
        return True

    def __repr__(self):
        return str(self.value)

