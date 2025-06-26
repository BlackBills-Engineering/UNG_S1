import serial, threading, time, logging
from .config import *

_log = logging.getLogger("driver")

def crc16(data: bytes) -> int:
    crc = CRC_INIT
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ CRC_POLY) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc

class Driver:
    STX, ETX, SF = 0x02, 0x03, 0xFA      # 0xFA обязателен!

    def __init__(self):
        self.uart = serial.Serial(SERIAL_PORT, BAUDRATE, BYTESIZE,
                                  PARITY, STOPBITS, timeout=TIMEOUT)
        self.lock, self.seq = threading.Lock(), 0x00
        _log.info(f"Serial {SERIAL_PORT} @ {BAUDRATE}bps opened")

    def _frame(self, addr: int, body: bytes) -> bytes:
        hdr = bytes([addr, 0xF0, self.seq, len(body)]) + body
        self.seq ^= 0x80
        crc = crc16(hdr)
        return bytes([self.STX]) + hdr + bytes([crc & 0xFF, crc >> 8, self.ETX, self.SF])

    def transact(self, addr: int, body: bytes, tmo=1.0) -> bytes:
        tx = self._frame(addr, body)
        with self.lock:
            self.uart.write(tx); self.uart.flush()
            start, buf = time.time(), bytearray()
            while time.time() - start < tmo:
                chunk = self.uart.read(self.uart.in_waiting or 1)
                if chunk:
                    buf += chunk
                    if buf[-2:] == bytes([self.ETX, self.SF]):
                        break
        return bytes(buf)

driver = Driver()
