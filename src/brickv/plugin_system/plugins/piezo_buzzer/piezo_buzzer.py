# -*- coding: utf-8 -*-  
"""
Piezo Buzzer Plugin
Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>

humidity.py: Piezo Buzzer Plugin Implementation

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
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt4.QtCore import pyqtSignal
        
import bricklet_piezo_buzzer
        
class PiezoBuzzer(PluginBase):
    qtcb_beep_finished = pyqtSignal()
    qtcb_morse_finished = pyqtSignal()
    
    def __init__ (self, ipcon, uid):
        PluginBase.__init__(self, ipcon, uid)
        
        self.pb = bricklet_piezo_buzzer.PiezoBuzzer(self.uid)
        self.ipcon.add_device(self.pb)
        self.version = '.'.join(map(str, self.pb.get_version()[1]))
        
        self.qtcb_beep_finished.connect(self.cb_beep)
        self.pb.register_callback(self.pb.CALLBACK_BEEP_FINISHED,
                                  self.qtcb_beep_finished.emit)
        self.qtcb_morse_finished.connect(self.cb_morse)
        self.pb.register_callback(self.pb.CALLBACK_MORSE_CODE_FINISHED,
                                  self.qtcb_morse_finished.emit)
        
        self.beep_edit = QLineEdit()
        self.beep_edit.setText(str(1000))
        self.beep_label = QLabel('Duration (ms): ')
        self.beep_button = QPushButton('Send Beep')
        self.beep_layout = QHBoxLayout()
        self.beep_layout.addWidget(self.beep_label)
        self.beep_layout.addWidget(self.beep_edit)
        self.beep_layout.addWidget(self.beep_button)
        
        self.morse_edit = QLineEdit()
        self.morse_edit.setText('- .. -. -.- . .-. ..-. --- .-. --. .')
        self.morse_edit.setMaxLength(60)
        self.morse_label = QLabel('Morse Code: ')
        self.morse_button = QPushButton('Send Morse Code')
        self.morse_layout = QHBoxLayout()
        self.morse_layout.addWidget(self.morse_label)
        self.morse_layout.addWidget(self.morse_edit)
        self.morse_layout.addWidget(self.morse_button)
        
        self.status_label = QLabel('')
        
        self.beep_button.pressed.connect(self.beep_pressed)
        self.morse_button.pressed.connect(self.morse_pressed)
        
        layout = QVBoxLayout(self)
        layout.addLayout(self.beep_layout)
        layout.addLayout(self.morse_layout)
        layout.addWidget(self.status_label)
        layout.addStretch()

    def start(self):
        pass
        
    def stop(self):
        pass

    @staticmethod
    def has_name(name):
        return 'Piezo Buzzer Bricklet' in name 
    
    def cb_beep(self):
        self.beep_button.setDisabled(False)
        self.morse_button.setDisabled(False)
        self.status_label.setText('')
        
    def cb_morse(self):
        self.beep_button.setDisabled(False)
        self.morse_button.setDisabled(False)
        self.status_label.setText('')
    
    def beep_pressed(self):
        duration = int(self.beep_edit.text())
        try:
            self.pb.beep(duration)
        except ip_connection.Error:
            return
        
        self.beep_button.setDisabled(True)
        self.morse_button.setDisabled(True)
        self.status_label.setText('Beeping...')        
        
    def morse_pressed(self):
        morse = str(self.morse_edit.text())
        try:
            self.pb.morse_code(morse)
        except ip_connection.Error:
            return
        
        self.beep_button.setDisabled(True)
        self.morse_button.setDisabled(True)
        self.status_label.setText('Beeping...')