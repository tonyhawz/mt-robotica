#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# USB comunication with USB4butia (USB4all) board
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


import usb

USB4ALL_VENDOR        = 0x04d8
USB4ALL_PRODUCT       = 0x000c
USB4ALL_CONFIGURATION = 1
USB4ALL_INTERFACE     = 0

ADMIN_MODULE_IN_ENDPOINT = 0x01
ADMIN_MODULE_OUT_ENDPOINT = 0x81

READ_HEADER_SIZE      = 3

TIMEOUT = 250

ERROR = -1

class usb_device():

    def __init__(self, dev):
        self.device = dev
        self.handle = None
        self.debug = True

    def open_device(self):
        """
        Open the baseboard, configure the interface
        """
        try:
            self.handle = self.device.open()
            self.handle.setConfiguration(USB4ALL_CONFIGURATION)
            self.handle.claimInterface(USB4ALL_INTERFACE)
        except usb.USBError, err:
            if self.debug:
                print err
            self.handle = None
            raise
        return self.handle

    def close_device(self):
        """
        Close the comunication with the baseboard
        """
        try:
            if self.handle:
                self.handle.releaseInterface()
        except Exception, err:
            if self.debug:
                print err
            raise
        self.handle = None
        self.device = None

    def read(self, length):
        """
        Read from the device length bytes
        """
        try:
            return self.handle.bulkRead(ADMIN_MODULE_OUT_ENDPOINT, length, TIMEOUT)
        except:
            if self.debug:
                print 'Exception in read usb'
            raise
 
    def write(self, data):
        """
        Write in the device: data
        """
        try:
            return self.handle.bulkWrite(ADMIN_MODULE_IN_ENDPOINT, data, TIMEOUT)
        except:
            if self.debug:
                print 'Exception in write usb'
            raise

    def get_info(self):
        """
        Get the device info such as manufacturer, etc
        """
        try:
            names = self.handle.getString(1, 255)
            copy = self.handle.getString(2, 255)
            sn = self.handle.getString(3, 255)
            return [names, copy, sn]
        except Exception, err:
            if self.debug:
                print 'Exception in get_info', err
            raise

def find():
    """
    List all busses and returns a list of baseboards detected
    """
    l = []
    try:
        for bus in usb.busses():
            for dev in bus.devices:
                if dev.idVendor == USB4ALL_VENDOR and dev.idProduct == USB4ALL_PRODUCT:
                    l.append(usb_device(dev))
    except Exception, err:
        if self.debug:
            print 'find gives the error:', err
    return l

