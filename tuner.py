class Tuner:
    def __init__(self, data=None):
        if data == None:
            self.data = [0] * 12
        else:
            self.data = data

    def set_data(self, data):
        self.data = data
        print(self.data)

    def is_auto(self):
        if int(str(self.data[1]), 16) == 1:
            return 1
        return 0

    def is_manual(self):
        if int(str(self.data[1]), 16) == 2:
            return 1
        return 0

    def is_bypass(self):
        if int(str(self.data[1]), 16) == 3:
            return 1
        return 0

    def get_antenna(self):
        return (int(str(self.data[5]), 16) & 0x0F) >> 2

    def get_frequency(self):
        return int(str(self.data[2]), 16) << 8 | int(str(self.data[3]), 16)

    def get_capacitance(self):
        return int(str(self.data[4]), 16)

    def get_inductance(self):
        return int(str(self.data[6]), 16)

    def get_power(self):
        return int(str(self.data[8]), 16)

    def get_vswr(self):
        return (int(str(self.data[9]), 16) << 8 | int(str(self.data[10]), 16)) / 100

    def create_command(self, **kwargs):
        cmd = []
        for arg in kwargs.values():
            cmd.append(arg)
        return cmd

    def set_antenna(self, port=0, var=0):
        if port > 0 and port < 4:
            port = port + 48
            return self.create_command(
                mnemonic=b"\x7a", port=bytes([port]), var=bytes([var])
            )
        else:
            return None

    def set_auto(self):
        return self.create_command(mnemonic=b"\x7a", var1=b"\x61", var2=bytes([0]))

    def set_bypass(self):
        return self.create_command(mnemonic=b"\x7a", var1=b"\x62", var2=bytes([0]))
