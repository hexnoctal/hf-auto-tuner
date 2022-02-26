import serial

RX_FRAME1 = b"\x77"
TX_FRAME1 = b"\x7a"


class RS232Handler:
    def __init__(self, port=None):
        self.port = port
        self.rxdata = [0] * 12
        self.sp = ""

    def open_serial(self, port="/dev/ttyUSB0"):
        self.sp = serial.Serial(
            port,
            "4800",
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=1,
        )
        try:
            self.sp.is_open
        except SerialException:
            print("Can't read %s" % port_cfg["device"])
            return None
        self.sp.setDTR(True)
        return self.sp

    def serial_rx_handler(self):
        """reads serial port"""
        buffer = []
        while True:
            try:
                ch = self.sp.read(1)
                if ch == RX_FRAME1:
                    buffer.append(ch)
                    for n in range(11):
                        buffer.append(self.sp.read(1))
                    chk = int()
                    for n in range(0, 11):
                        chk += int.from_bytes(buffer[n], "big")
                    chk = (chk ^ 0xFF) & 0x00FF
                    if (chk + 1) == int.from_bytes(buffer[-1], "big"):
                        for n in range(0, 12):
                            self.rxdata[n] = hex(int.from_bytes(buffer[n], "big"))
                buffer = []
            except Exception as e:
                print(f"serial_handler exception {e}")
                pass

    def serial_tx_handler(self, data=None):
        chk = 0
        for n in range(len(data)):
            chk += int.from_bytes(data[n], "big")
        chk = (chk ^ 0xFF) + 1
        data.append(bytes([chk]))
        for byte in data:
            self.sp.write(byte)
