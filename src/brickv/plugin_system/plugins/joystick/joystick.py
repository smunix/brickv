# -*- coding: utf-8 -*-  
"""
Joystick Plugin
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

joystick.py: Joystick Plugin implementation

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

from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPainter, QPushButton, QBrush
from PyQt4.QtCore import pyqtSignal, Qt

import bricklet_joystick

class PositionLabel(QLabel):
    def setText(self, text):
        text = "Position: " + text
        super(PositionLabel, self).setText(text)
        
class JoystickFrame(QFrame):
    def __init__(self, parent = None):
        QFrame.__init__(self, parent)
        self.x = 0
        self.y = 0
        self.pressed = False
        
    def set_pressed(self, pressed):
        self.pressed = pressed
        self.repaint()
        
    def set_position(self, x, y):
        self.x = x + 110
        self.y = 110 - y
        self.repaint()
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.pressed:
            qp.setBrush(QBrush(Qt.red))
        else:
            qp.setBrush(Qt.NoBrush)
        qp.setPen(Qt.red)
        qp.drawLine(110, 10, 110, 210)
        qp.drawLine(10, 110, 210, 110)
        qp.drawEllipse(self.x-5, self.y-5, 10, 10)
        qp.end()
        
class Joystick(PluginBase):
    qtcb_position = pyqtSignal(int, int)
    qtcb_pressed = pyqtSignal()
    qtcb_released = pyqtSignal()
    
    def __init__ (self, ipcon, uid):
        PluginBase.__init__(self, ipcon, uid)
        
        self.js = bricklet_joystick.Joystick(self.uid)
        self.ipcon.add_device(self.js)
        self.version = '.'.join(map(str, self.js.get_version()[1]))
        
        self.qtcb_position.connect(self.cb_position)
        self.js.register_callback(self.js.CALLBACK_POSITION,
                                  self.qtcb_position.emit)
        
        self.qtcb_pressed.connect(self.cb_pressed)
        self.js.register_callback(self.js.CALLBACK_PRESSED,
                                  self.qtcb_pressed.emit)
        
        self.qtcb_released.connect(self.cb_released)
        self.js.register_callback(self.js.CALLBACK_RELEASED,
                                  self.qtcb_released.emit)
        
        self.joystick_frame = JoystickFrame(self)
        self.joystick_frame.setMinimumSize(220, 220)
        self.joystick_frame.setMaximumSize(220, 220)
        self.joystick_frame.set_position(0, 0)
       
        self.calibration_button = QPushButton('Calibrate (0, 0)')
        self.position_label = PositionLabel('Position: (0, 0)')
        
        self.calibration_button.pressed.connect(self.calibration_pressed)
        
        self.current_x = 0
        self.current_y = 0
        
        plot_list = [['X', Qt.darkGreen, self.get_current_x],
                     ['Y', Qt.blue, self.get_current_y]]
        self.plot_widget = PlotWidget('Position', plot_list)
        
        layout_h1 = QHBoxLayout()
        layout_h1.addStretch()
        layout_h1.addWidget(self.position_label)
        layout_h1.addStretch()

        layout_h2 = QHBoxLayout()
        layout_h2.addStretch()
        layout_h2.addWidget(self.joystick_frame)
        layout_h2.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h1)
        layout.addLayout(layout_h2)
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.calibration_button)

    def start(self):
        try:
            self.js.set_position_callback_period(20)
        except ip_connection.Error:
            return
        
        self.plot_widget.stop = False
        
    def stop(self):
        try:
            self.js.set_position_callback_period(0)
        except ip_connection.Error:
            pass
        
        self.plot_widget.stop = True

    @staticmethod
    def has_name(name):
        return 'Joystick Bricklet' in name 

    def calibration_pressed(self):
        try:
            self.js.calibrate()
        except ip_connection.Error:
            return
        
    def get_current_x(self):
        return self.current_x
    
    def get_current_y(self):
        return self.current_y

    def cb_pressed(self):
        self.joystick_frame.set_pressed(True)
        
    def cb_released(self):
        self.joystick_frame.set_pressed(False)

    def cb_position(self, x, y):
        self.current_x = x
        self.current_y = y
        self.position_label.setText(str((x, y)))
        self.joystick_frame.set_position(x, y)