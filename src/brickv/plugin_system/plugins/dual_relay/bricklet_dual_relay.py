# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2011-10-06.      #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################

try:
    from collections import namedtuple
except ImportError:
    from ip_connection import namedtuple
from ip_connection import Device, IPConnection, Error

GetState = namedtuple('State', ['relay1', 'relay2'])
GetVersion = namedtuple('Version', ['name', 'firmware_version', 'binding_version'])

class DualRelay(Device):

    TYPE_SET_STATE = 1
    TYPE_GET_STATE = 2

    def __init__(self, uid):
        Device.__init__(self, uid)

        self.binding_version = [1, 0, 0]


    def get_version(self):
        return GetVersion(self.name, self.firmware_version, self.binding_version)

    def set_state(self, relay1, relay2):
        self.ipcon.write(self, DualRelay.TYPE_SET_STATE, (relay1, relay2), '? ?', '')

    def get_state(self):
        return GetState(*self.ipcon.write(self, DualRelay.TYPE_GET_STATE, (), '', '? ?'))
