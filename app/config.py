# RS-485
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE    = 9600
BYTESIZE    = 8
PARITY      = "E"        # ODD parity
STOPBITS    = 1
TIMEOUT     = 0.3        # sec

# CRC-16/CCITT
CRC_INIT = 0x0000
CRC_POLY = 0x1021

# единственная колонка: pump_id = 1  →  адрес 0x51
DEFAULT_PUMP_IDS = [1]
