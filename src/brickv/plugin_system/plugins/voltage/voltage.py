# -*- coding: utf-8 -*-  
"""
Voltage Plugin
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

voltage.py: Voltage Plugin Implementation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation; either version 2 
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from plugin_system.plugin_base import PluginBase
import ip_connection
from plot_widget import PlotWidget

from PyQt4.QtGui import QVBoxLayout, QLabel, QHBoxLayout
from PyQt4.QtCore import pyqtSignal, Qt
        
import bricklet_voltage
        
class CurrentLabel(QLabel):
    def setText(self, text):
        text = "Voltage: " + text + " V"
        super(CurrentLabel, self).setText(text)
    
class Voltage(PluginBase):
    qtcb_voltage = pyqtSignal(int)
    
    def __init__ (self, ipcon, uid):
        PluginBase.__init__(self, ipcon, uid)
        
        self.vol = bricklet_voltage.Voltage(self.uid)
        self.ipcon.add_device(self.vol)
        self.version = '.'.join(map(str, self.vol.get_version()[1]))
        
        self.qtcb_voltage.connect(self.cb_voltage)
        self.vol.register_callback(self.vol.CALLBACK_VOLTAGE,
                                   self.qtcb_voltage.emit) 
        
        self.voltage_label = CurrentLabel('Voltage: ')
        
        self.current_value = 0
        
        plot_list = [['', Qt.red, self.get_current_value]]
        self.plot_widget = PlotWidget('Voltage [mV]', plot_list)
        
        layout_h = QHBoxLayout()
        layout_h.addStretch()
        layout_h.addWidget(self.voltage_label)
        layout_h.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h)
        layout.addWidget(self.plot_widget)
        
    def start(self):
        try:
            self.cb_voltage(self.vol.get_voltage())
            self.vol.set_voltage_callback_period(100)
        except ip_connection.Error:
            return
        
        self.plot_widget.stop = False
        
    def stop(self):
        try:
            self.vol.set_voltage_callback_period(0)
        except ip_connection.Error:
            pass
        
        self.plot_widget.stop = True

    @staticmethod
    def has_name(name):
        return 'Voltage Bricklet' in name 

    def get_current_value(self):
        return self.current_value

    def cb_voltage(self, voltage):
        self.current_value = voltage
        self.voltage_label.setText(str(voltage/1000.0)) 