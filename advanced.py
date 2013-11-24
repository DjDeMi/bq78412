#!/usr/bin/env python3.3
# coding= utf-8
from gi.repository import Gtk
from exceptions import *

class AdvancedWindow(Gtk.Window):

    def __init__(self, parent, device):
        Gtk.Window.__init__(self)
        self.device = device
        self.parent = parent

        self.set_title("Advanced Settings")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_transient_for(parent)
        self.set_modal(True)

        vbox = Gtk.VBox(False)
        vbox.set_spacing(5)
        self.add(vbox)

        hbox_design_capacity = Gtk.HBox(False)
        vbox.pack_start(hbox_design_capacity, False, False, 0)

        design_capacity_button = Gtk.Button(label="Change Design Capacity")
        design_capacity_button.set_size_request(250, 50)
        design_capacity_button.connect("clicked", self.on_design_capacity_button_clicked)
        hbox_design_capacity.pack_start(design_capacity_button, False, False, 6)

        hbox_end_of_discharge_voltage = Gtk.HBox(False)
        vbox.pack_start(hbox_end_of_discharge_voltage, False, False, 0)

        discharge_voltage_button = Gtk.Button(label="Change End of Discharge Voltage")
        discharge_voltage_button.set_size_request(250, 50)
        discharge_voltage_button.connect("clicked", self.on_discharge_voltage_button_clicked)
        hbox_end_of_discharge_voltage.pack_start(discharge_voltage_button, False, False, 6)

        hbox_device_configuration_2 = Gtk.HBox(False)
        vbox.pack_start(hbox_device_configuration_2, False, False, 0)

        device_configuration_2_button = Gtk.Button(label="Change Device configuration 2")
        device_configuration_2_button.set_size_request(250, 50)
        device_configuration_2_button.connect("clicked", self.on_device_configuration_button_clicked)
        hbox_device_configuration_2.pack_start(device_configuration_2_button, False, False, 6)

        hbox_display_configuration1 = Gtk.HBox(False)
        vbox.pack_start(hbox_display_configuration1, False, False, 0)

        display_configuration_1_button = Gtk.Button(label="Change Display Configuration 1")
        display_configuration_1_button.set_size_request(250, 50)
        display_configuration_1_button.connect("clicked", self.on_display_configuration_1_button_clicked)
        hbox_display_configuration1.pack_start(display_configuration_1_button, False, False, 6)

        hbox_display_configuration2 = Gtk.HBox(False)
        vbox.pack_start(hbox_display_configuration2, False, False, 0)

        display_configuration_2_button = Gtk.Button(label="Change Display Configuration 2")
        display_configuration_2_button.set_size_request(250, 50)
        display_configuration_2_button.connect("clicked", self.on_display_configuration_2_button_clicked)
        hbox_display_configuration2.pack_start(display_configuration_2_button, False, False, 6)

        hbox_display_configuration3 = Gtk.HBox(False)
        vbox.pack_start(hbox_display_configuration3, False, False, 0)

        display_configuration_3_button = Gtk.Button(label="Change Display Configuration 3")
        display_configuration_3_button.set_size_request(250, 50)
        display_configuration_3_button.connect("clicked", self.on_display_configuration_3_button_clicked)
        hbox_display_configuration3.pack_start(display_configuration_3_button, False, False, 6)

        hbox_display_configuration4 = Gtk.HBox(False)
        vbox.pack_start(hbox_display_configuration4, False, False, 0)

        display_configuration_4_button = Gtk.Button(label="Change Display Configuration 4")
        display_configuration_4_button.set_size_request(250, 50)
        display_configuration_4_button.connect("clicked", self.on_display_configuration_4_button_clicked)
        hbox_display_configuration4.pack_start(display_configuration_4_button, False, False, 6)

        hbox_display_configuration5 = Gtk.HBox(False)
        vbox.pack_start(hbox_display_configuration5, False, False, 0)

        display_configuration_5_button = Gtk.Button(label="Change Display Configuration 5")
        display_configuration_5_button.set_size_request(250, 50)
        display_configuration_5_button.connect("clicked", self.on_display_configuration_5_button_clicked)
        hbox_display_configuration5.pack_start(display_configuration_5_button, False, False, 6)

    def on_design_capacity_button_clicked(self, button):
        # between 1 to 3270
        print("Design Capacity")
        while True:
            value = self.get_value("Insert value between 1 to 3270", "Change design capacity")
            print(value)
            if(value != None):
                if(1<=int(value,10)<=3270):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Value must be between 1 to 3270. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a value between 1 to 3270. \n Try again.")
        value = value.zfill(4)
        print(value)
        print(len(hex(int(value,10))[2:]))
        hex_value = hex(int(value,10))[2:].zfill(4).upper()
        print(hex_value)
        convert_string = "FF172440" + hex_value[2:4] + hex_value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x24\x40\x01\x00\x73")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def on_discharge_voltage_button_clicked(self, button):
        # between 4000 to 65535
        print("Discharge Voltage")
        while True:
            value = self.get_value("Insert value between 4000 to 65535", "Change End of Discharge Voltage")
            print(value)
            if(value != None):
                if(4000<=int(value,10)<=65535):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Value must be between 4000 to 65535. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a value between 4000 to 65535. \n Try again.")
        value = value.zfill(4)
        print(value)
        print(len(hex(int(value,10))[2:]))
        hex_value = hex(int(value,10))[2:].zfill(4).upper()
        print(hex_value)
        convert_string = "FF172C40" + hex_value[2:4] + hex_value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x2C\x40\x01\x00\x7B")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")


    def on_device_configuration_button_clicked(self, button):
        # between 0000 to BFFF
        print("Device Configuration")
        while True:
            value = self.get_value("Insert hex value between 0000 to BFFF", "Change Device Configuration 2")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(BFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to BFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to BFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF173C40" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x3C\x40\x01\x00\x6B")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")


    def on_display_configuration_1_button_clicked(self, button):
        # between 0000 to FFFF
        print("Display Configuration 1")
        while True:
            value = self.get_value("Insert hex value between 0000 to FFFF", "Change Display Configuration 1")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(FFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to FFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to FFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF173E40" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x3E\x40\x01\x00\x69")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def on_display_configuration_2_button_clicked(self, button):
        # between 0000 to FFFF
        print("Display Configuration 2")
        while True:
            value = self.get_value("Insert hex value between 0000 to FFFF", "Change Display Configuration 2")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(FFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to FFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to FFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF174040" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x40\x40\x01\x00\x17")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def on_display_configuration_3_button_clicked(self, button):
        # between 0000 to FFFF
        print("Display Configuration 3")
        while True:
            value = self.get_value("Insert hex value between 0000 to FFFF", "Change Display Configuration 3")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(FFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to FFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to FFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF174240" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x42\x40\x01\x00\x15")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def on_display_configuration_4_button_clicked(self, button):
        # between 0000 to FFFF
        print("Display Configuration 4")
        while True:
            value = self.get_value("Insert hex value between 0000 to FFFF", "Change Display Configuration 4")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(FFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to FFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to FFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF174440" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x44\x40\x01\x00\x13")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def on_display_configuration_5_button_clicked(self, button):
        # between 0000 to FFFF
        print("Display Configuration 5")
        while True:
            value = self.get_value("Insert hex value between 0000 to FFFF", "Change Display Configuration 5")
            print(value)
            if(value != None):
                if(0<=int(value,10)<=int(FFFF,16)):
                    print("Balio zuzena, ez da None")
                    break
                else:
                    print("Balio desegokia")
                    self.error_message("Data error", "Hex value must be between 0000 to FFFF. \n Try again.")
            else:
                print("None")
                self.error_message("Data error", "You need insert a hex value between 0000 to FFFF. \n Try again.")
        value = value.zfill(4)
        convert_string = "FF174640" + value[2:4] + value[0:2]
        print(convert_string)
        hex_value_string = bytearray.fromhex(convert_string)
        convert_string += hex(self.crc(hex_value_string))[2:].upper()
        hex_value_string = bytearray.fromhex(convert_string)
        print(hex_value_string)
        self.device.send_command(hex_value_string)
        try:
            raw_data = self.device.read_input(3)
            print("ACK irakurrita ")
            print(raw_data)
        except ACKError:
            self.error_message("Data error", "Received data has not ACK")
        except CRCError:
            self.error_message("Data error", "Received CRC is not correct")
        except sizeError:
            self.error_message("Data error", "Received data has not correct size")
        except timeoutError:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            self.device.send_command(b"\xFF\x16\x46\x40\x01\x00\x11")
            try:
                raw_data = self.device.read_input(5)
                print("Balioak irakurrita ")
                print(raw_data)
            except ACKError:
                self.error_message("Data error", "Received data has not ACK")
            except CRCError:
                self.error_message("Data error", "Received CRC is not correct")
            except sizeError:
                self.error_message("Data error", "Received data has not correct size")
            except timeoutError:
                self.error_message("Timeout", "The device doesn't respond.")
            else:
                if ((raw_data[3] << 8) + raw_data[2]) == ((hex_value_string[5] << 8) + hex_value_string[4]):
                    self.info_message("Correct", "The change has been done correctly")
                else:
                    self.error_message("Error", "Something will be wrong.\n Try again")

    def get_value(parent, message, title=''):
        # Returns user input as a string or None
        # If user does not input text it returns None, NOT AN EMPTY STRING.
        dialogWindow = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, message)

        dialogWindow.set_title(title)

        dialogBox = dialogWindow.get_content_area()
        userEntry = Gtk.Entry()
        userEntry.set_size_request(250,0)
        dialogBox.pack_end(userEntry, False, False, 0)

        dialogWindow.show_all()
        response = dialogWindow.run()
        text = userEntry.get_text() 
        dialogWindow.destroy()
        if (response == Gtk.ResponseType.OK) and (text != ''):
            return text
        else:
            return None

    def error_message(self, firstMessage, secondMessage):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, str(firstMessage))
        dialog.format_secondary_text(str(secondMessage))
        dialog.run()
        dialog.destroy()

    def info_message(self, firstMessage, secondMessage):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, str(firstMessage))
        dialog.format_secondary_text(str(secondMessage))
        dialog.run()
        dialog.destroy()

    def crc(self, data):
        result = 0
        for c in data[1:]:
            result = result ^ c
        return result