from .driver import driver

class Core:
    ADR = staticmethod(lambda pid: 0x50 + pid)

    @staticmethod
    def _bcd4(val: float) -> bytes:              # 123.45 → b'\x01\x23\x45\x00'
        i = int(round(val * 100))
        return bytes(int(f"{i:08d}"[j:j+2]) for j in range(0, 8, 2))

    # CD5 – цены: price1 (левая сторона), price9 (правая)
    @classmethod
    def price(cls, pid: int, price1: float, price9: float):
        payload = b''.join(cls._bcd4(price1) if i == 0 else
                           cls._bcd4(price9) if i == 8 else b'\x00\x00\x00'
                           for i in range(0, 48, 3))
        driver.transact(cls.ADR(pid), bytes([0x05, len(payload)]) + payload)

    # CD3 + AUTHORIZE (ровно N литров)
    @classmethod
    def authorize(cls, pid: int, liters: float):
        driver.transact(cls.ADR(pid), bytes([0x03, 0x04]) + cls._bcd4(liters))
        driver.transact(cls.ADR(pid), bytes([0x01, 0x01, 0x06]))

    @classmethod
    def stop(cls, pid: int):
        driver.transact(cls.ADR(pid), bytes([0x01, 0x01, 0x07]))

    @classmethod
    def reset(cls, pid: int):
        driver.transact(cls.ADR(pid), bytes([0x01, 0x01, 0x05]))
