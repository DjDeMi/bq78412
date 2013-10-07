from serial import Serial, SerialException
from sys import stderr, exit

class Device:

    def __init__(self, address, bitrate):
        try:
            self.device = Serial(address, bitrate)
        except SerialException:
            stderr.write("Error connecting to " + address + ".\n")
            exit(1)

    def get_data(self):
        self.send_command(b"\xFF\x16\x00\x00\x1A\x00\x0C")
        raw_data = self.read_input(27)
        data = self.parse_data(raw_data)
        return data

    def reset_rsoc(self):
        self.send_command(b"\xFF\x13\x05\x00\x00\x64\x8D")
        raw_data = self.read_input(3)
        return True

    def send_command(self, command):
        self.device.write(command)

    def read_input(self, size):
        raw_data = self.device.read(size)
        if len(raw_data) != 0:
            if self.crc(raw_data) and self.ack(raw_data):
                return raw_data
        return None

    def parse_data(self, raw_data):
        data = {}
        data['voltage'] = (raw_data[6] << 8) + raw_data[5]
        data['current'] = ((raw_data[8] << 8) + raw_data[7])/100
        data['avg_current'] = ((raw_data[18] << 8) + raw_data[17])/100
        data['temperature'] = (raw_data[4] << 8) + raw_data[3]
        data['rsoc'] = (raw_data[24] << 8) + raw_data[23]
        return data

    def crc(self, data):
        result = 0
        for c in data[:-1]:
            result = result ^ c
        return result == data[-1]

    def ack(self, data):
        return data[1] == 33
