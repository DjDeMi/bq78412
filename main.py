# coding= utf-8
#!/usr/bin/env python3.3
from gi.repository import Gtk, GObject
from bq78412 import Device
from arguments import *
from exceptions import *
import logging

class MainWindow(Gtk.Window):

    def __init__(self, device, tbd):
        Gtk.Window.__init__(self)
        self.device = device
        self.timebetweendata = tbd

        self.set_title("bq78412")
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.VBox(False)
        self.add(vbox)

        # voltage hbox
        hbox_voltage = Gtk.HBox(False)
        vbox.pack_start(hbox_voltage, False, False, 0)

        voltage_label = Gtk.Label("Voltage")
        voltage_label.set_size_request(100, 50)
        hbox_voltage.pack_start(voltage_label, False, False, 6)

        self.voltage_value = Gtk.Label(0)
        self.voltage_value.set_size_request(100, 50)
        hbox_voltage.pack_start(self.voltage_value, False, False, 6)

        voltage_unit = Gtk.Label("mV")
        voltage_unit.set_size_request(100, 50)
        hbox_voltage.pack_start(voltage_unit, False, False, 6)

        # current hbox
        hbox_current = Gtk.HBox(False)
        vbox.pack_start(hbox_current, False, False, 0)

        current_label = Gtk.Label("Current")
        current_label.set_size_request(100, 50)
        hbox_current.pack_start(current_label, False, False, 6)

        self.current_value = Gtk.Label(0)
        self.current_value.set_size_request(100, 50)
        hbox_current.pack_start(self.current_value, False, False, 6)

        current_unit = Gtk.Label("mA")
        current_unit.set_size_request(100, 50)
        hbox_current.pack_start(current_unit, False, False, 6)

        # avg_current hbox
        hbox_avg_current = Gtk.HBox(False)
        vbox.pack_start(hbox_avg_current, False, False, 0)

        avg_current_label = Gtk.Label("Avg. current")
        avg_current_label.set_size_request(100, 50)
        hbox_avg_current.pack_start(avg_current_label, False, False, 6)

        self.avg_current_value = Gtk.Label(0)
        self.avg_current_value.set_size_request(100, 50)
        hbox_avg_current.pack_start(self.avg_current_value, False, False, 6)

        avg_current_unit = Gtk.Label("mA")
        avg_current_unit.set_size_request(100, 50)
        hbox_avg_current.pack_start(avg_current_unit, False, False, 6)

        # temperature hbox
        hbox_temperature = Gtk.HBox(False)
        vbox.pack_start(hbox_temperature, False, False, 0)

        temperature_label = Gtk.Label("Temperature")
        temperature_label.set_size_request(100, 50)
        hbox_temperature.pack_start(temperature_label, False, False, 6)

        self.temperature_value = Gtk.Label(0)
        self.temperature_value.set_size_request(100, 50)
        hbox_temperature.pack_start(self.temperature_value, False, False, 6)

        temperature_unit = Gtk.Label("ºC")
        temperature_unit.set_size_request(100, 50)
        hbox_temperature.pack_start(temperature_unit, False, False, 6)

        # rsoc hbox
        hbox_rsoc = Gtk.HBox(False)
        vbox.pack_start(hbox_rsoc, False, False, 0)

        rsoc_label = Gtk.Label("RSOC")
        rsoc_label.set_size_request(100, 50)
        hbox_rsoc.pack_start(rsoc_label, False, False, 6)

        self.rsoc_value = Gtk.Label(0)
        self.rsoc_value.set_size_request(100, 50)
        hbox_rsoc.pack_start(self.rsoc_value, False, False, 6)

        rsoc_unit = Gtk.Label("%")
        rsoc_unit.set_size_request(100, 50)
        hbox_rsoc.pack_start(rsoc_unit, False, False, 6)

        # refresh hbox
        hbox_refresh = Gtk.HBox(False)
        vbox.pack_start(hbox_refresh, False, False, 6)

        refresh_check = Gtk.CheckButton("Auto refresh")
        refresh_check.set_size_request(100, 50)
        refresh_check.connect("toggled", self.on_refresh_toggled)
        hbox_refresh.pack_start(refresh_check, False, False, 6)

        # buttons hbox
        hbox_buttons = Gtk.HBox(False)
        vbox.pack_start(hbox_buttons, False, False, 6)

        read_button = Gtk.Button(label="Read data")
        read_button.set_size_request(156, 50)
        read_button.connect("clicked", self.on_read_button_clicked)
        hbox_buttons.pack_start(read_button, False, False, 6)

        rsoc_button = Gtk.Button(label="RSOC 100%")
        rsoc_button.set_size_request(156, 50)
        rsoc_button.connect("clicked", self.on_rsoc_button_clicked)
        hbox_buttons.pack_start(rsoc_button, False, False, 6)

        # attributes
        self.refresh = False

    def on_read_button_clicked(self, button):
        self.update_data()

    def on_rsoc_button_clicked(self, button):
        try:
            self.device.reset_rsoc()
        except incorrect_ack:
            self.error_message("Data error", "Received data has not ACK")
        except incorrect_crc:
            self.error_message("Data error", "Received CRC is not correct")
        except incorrect_size:
            self.error_message("Data error", "Received data has not correct size")
        except timeout_except:
            self.error_message("Timeout", "The device doesn't respond.")
        else:
            logging.debug("aaa")
            self.update_data()
            logging.debug("rsoc reset")

    def on_refresh_toggled(self, refresh_check):
        self.refresh = refresh_check.get_active()
        if self.refresh:
            GObject.timeout_add(self.timebetweendata*1000, self.refresh_data(refresh_check))

    def refresh_data(self, refresh_check):
        if self.refresh:
            self.update_data(refresh_check)
        return self.refresh
    
    def error_message(self, firstMessage, secondMessage):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, str(firstMessage))
        dialog.format_secondary_text(str(secondMessage))
        dialog.run()
        logging.debug("ERROR dialog closed")
        dialog.destroy()

    def update_data(self, refresh_check=None):
        try:
            logging.debug("Refresh value check " + str(refresh_check))
            logging.debug("Refresh value " + str(self.refresh))
            data = self.get_data()
        except incorrect_ack:
            self.error_message("Data error", "Received data has not ACK")
            if refresh_check != None:
                refresh_check.set_active(False)
                self.refresh = False
        except incorrect_crc:
            self.error_message("Data error", "Received CRC is not correct")
            if refresh_check != None:
                refresh_check.set_active(False)
                self.refresh = False
        except incorrect_size:
            self.error_message("Data error", "Received data has not correct size")
            if refresh_check != None:
                refresh_check.set_active(False)
                self.refresh = False
        except timeout_except:
            self.error_message("Timeout", "The device doesn't respond.")
            if refresh_check != None:
                refresh_check.set_active(False)
                self.refresh = False
            logging.debug("Refresh value check" + str(refresh_check))
            logging.debug("Refresh value " + str(self.refresh))
        else:
            self.voltage_value.set_text(str(data['voltage']))
            self.current_value.set_text(str(data['current']))
            self.avg_current_value.set_text(str(data['avg_current']))
            self.temperature_value.set_text(str(data['temperature']))
            self.rsoc_value.set_text(str(data['rsoc']))
            logging.debug("data updated with: "+str(data))
            

    def get_data(self):
        return self.device.get_data()

args = read_arguments()
if args['verbose']:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    
logging.debug("Received args: "+ str(args))
logging.debug("Trying to connect")
device = Device(args['port'], args['timeout'], 9600)
win = MainWindow(device, args['timebetweendata'])
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
