# fatek_plc_wrapper

Wrapper to read multiple Fatek formatted addresses via Modbus protocol

List of different types can be provided, then dict with result is returned.

main read() function is detecting type of each address of the list and associate is to proper Modbus function.

Number of each function runs is optimzed by configuring following ModbusClientWrapper class parameters:
```
    COILS_MAX_READ_SIZE = 2000
    DISCRETE_INPUTS_MAX_READ_SIZE = 2000
    HOLDING_REGISTERS_MAX_READ_SIZE = 125
    INPUT_REGISTERS_MAX_READ_SIZE = 125
```

## Use case:
normally to read R100, R200, Y0, Y50 and Y99, T105 values, x6 modbus queries are requred.
```
read_coils(0, 1)
read_coils(50, 1)
read_coils(99, 1)
read_coils(9105, 1)
read_holding_registers(100, 1)
read_holding_registers(200, 1)

```

With configured 
```
COILS_MAX_READ_SIZE = 100
HOLDING_REGISTERS_MAX_READ_SIZE = 101
```
read is optmized following reads:
```
read_coils(0, 100)
read_coils(9105, 1)
read_holding_resters(100, 101)
```

## Example for above scenario:

for above scenario following example is returned:
```python
pip install -r requirements.txt

python

from fatek_modbus_client import FatekModbusClient

client = FatekModbusClient("192.168.10.230")
client.read(["Y0", "T105", "Y50",  "R200", "Y99", "R100"])
{'Y0': False, 'Y50': False, 'Y99': False, 'T105': False, 'R200': 1, 'R100': 0}

```

## Fatek table

| Modbus | FATEK | Description |
| ------ | ----- | -----------
| 000001～000256 | Y0～Y255 | Discrete Output
| 001001～001256 | X0～X255 | Discrete Input
| 002001～004002 | M0～M2001 | Discrete M Relay
| 006001～007000 | S0～S999 | Discrete S Relay
| 009001～009256 | T0～T255 | Status of T0～T255
| 009501～009756 | C0～C255 | Status of C0～C255
| 400001～404168 | R0～R4167 | Holding Register
| 405001～405999 | R5000～R5998 | Holding Register or ROR
| 406001～408999 | D0～D2998 Data | Register
| 409001～409256 | T0～T255 | Current Value of T0～T255
| 409501～409700 | C0～C199 | Current Value of C0～C199( 16-bit)
| 409701～409812 | C200～C255 | Current Value of C200～C255( 32-bit)