#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Device abstraction for USB4butia
#
# Copyright (c) 2012-2013 Butiá Team butia@fing.edu.uy 
# Butia is a free and open robotic platform
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingeniería - Universidad de la República - Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


NULL_BYTE = 0x00
OPEN_COMMAND = 0x00
CLOSE_COMMAND = 0x01
HEADER_PACKET_SIZE = 0x06

ADMIN_HANDLER_SEND_COMMAND = 0x00

OPEN_RESPONSE_PACKET_SIZE = 5
CLOSE_RESPONSE_PACKET_SIZE = 2

READ_HEADER_SIZE = 3
MAX_BYTES = 64

ERROR = -1

class Device():

    def __init__(self, baseboard, name, handler=None):
        self.baseboard = baseboard
        self.name = name
        self.handler = handler
        if not(self.handler == None):
            self.handler_tosend = self.handler * 8
        self.functions = {}
        self.debug = False

    def add_functions(self, func_list):
        """
        Add the functions to current device
        """
        for f in func_list:
            self.functions[f['name']] = f

    def module_send(self, call, params_length, params):
        """
        Send to the device the specifiy call and parameters
        """
        if len(params) == 1:
            if type(params[0]) == str:
                params = to_ord(params[0])

        send_packet_length = 0x04 + len(params)

        w = []
        w.append(self.handler_tosend)
        w.append(send_packet_length)
        w.append(NULL_BYTE)
        w.append(call)
        for p in params:
            w.append(p)

        self.baseboard.dev.write(w)

    def module_read(self):
        """
        Read the device data
        """
        raw = self.baseboard.dev.read(MAX_BYTES)
        if self.debug:
            print 'device:module_rad return', raw
        if raw[1] == 5:
            if raw[4] == 255:
                return -1
            else:
                return raw[4]
        elif raw[1] == 6:
            return raw[4] + raw[5] * 256
        else:
            ret = ''
            for r in raw[4:]:
                if not(r == 0):
                    ret = ret + chr(r)
            return ret

    def module_open(self):
        """
        Open this device. Return the handler
        """
        module_name = to_ord(self.name)
        module_name.append(0)
        
        open_packet_length = HEADER_PACKET_SIZE + len(module_name) 

        module_in_endpoint  = 0x01
        module_out_endpoint = 0x01

        w = []
        w.append(ADMIN_HANDLER_SEND_COMMAND)
        w.append(open_packet_length)
        w.append(NULL_BYTE)
        w.append(OPEN_COMMAND)
        w.append(module_in_endpoint)
        w.append(module_out_endpoint)
        w = w + module_name
        self.baseboard.dev.write(w)

        raw = self.baseboard.dev.read(OPEN_RESPONSE_PACKET_SIZE)

        if self.debug:
            print 'device:module_open return', raw

        h = raw[4]
        self.handler = h
        self.handler_tosend = self.handler * 8
        return h

    def has_function(self, func):
        """
        Check if this device has func function
        """
        return self.functions.has_key(func)

    def call_function(self, func, params):
        """
        Call specify func function with params parameters
        """
        self.module_send(self.functions[func]['call'], self.functions[func]['params'], params)
        return self.module_read()

def to_ord(string):
    """
    Useful function to convert characters into ordinal Unicode
    """
    s = []
    for l in string:
        o = ord(l)
        if not(o == 0):
            s.append(o)
    return s

