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
        self.send_command("\xFF\x16\x00\x00\x1A\x00\x0C")
        raw_data = self.read_input()
        data = self.parse_data(raw_data)
        return data

    def reset_rsoc(self):
        return True

    def send_command(self, command):
        self.device.write(command)

    def read_input(self):
        raw_data = self.device.readline()
        data = []
        if len(raw_data) != 0:
            for c in raw_data:
                data.append(hex(ord(c)))
            if self.crc(data) and self.ack(data):
                return data
        return None

    def parse_data(self, raw_data):
        data = {}
        data['voltage'] = int(raw_data[6] + raw_data[5], 16)
        data['current'] = int(raw_data[8] + raw_data[7], 16)
        data['avg_current'] = int(raw_data[18] + raw_data[17], 16)
        data['temperature'] = int(raw_data[4] + raw_data[3], 16)
        data['rsoc'] = int(raw_data[24] + raw_data[23], 16)
        return data

    def crc(self, data):
        result = hex(0x00)
        for c in data[:-1]:
            result = hex(int(result, 16) ^ int(c, 16))
        return result == data[-1]

    def ack(self, data):
        return data[1] == '0x21'
