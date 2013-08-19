#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# USB4Butia main
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


import os
import imp
import com_usb
from baseboard import Baseboard
from device import Device

ERROR = -1

class USB4Butia():

    def __init__(self, debug=False, get_modules=True):
        self._debug = debug
        self._hotplug = []
        self._openables = []
        self._drivers_loaded = {}
        self._bb = []
        self._modules = []
        self._get_all_drivers()
        self.find_butias(get_modules)

    def get_butia_count(self):
        """
        Gets the number of boards detected
        """
        return len(self._bb)

    def find_butias(self, get_modules=True):
        """
        Search for connected USB4Butia boards and open it
        """
        devices = com_usb.find()
        for dev in devices:
            b = Baseboard(dev)
            try:
                b.open_baseboard()
                self._bb.append(b)
            except:
                if self._debug:
                    print 'error open baseboard'
        if get_modules:
            self.get_modules_list()

    def get_modules_list(self, normal=True):
        """
        Get the list of modules loaded in the board
        """
        self._modules = []
        n_boards = self.get_butia_count()

        if self._debug:
            print '=Listing Devices'

        for i, b in enumerate(self._bb):
            try:
                listi = b.get_listi()
                s = b.get_handler_size()

                if self._debug:
                    print '===board', i

                for m in range(0, s + 1):
                    module_name = listi[b.get_handler_type(m)]
                    if n_boards > 1:
                        complete_name = module_name + '@' + str(i) + ':' +  str(m)
                    else:
                        complete_name = module_name + ':' +  str(m)

                    if self._debug:
                        print '=====module', module_name, (8 - len(module_name)) * ' ', complete_name

                    if not(module_name == 'port'):

                        if normal:
                            self._modules.append(complete_name)
                        else:
                            self._modules.append((str(m), module_name, str(i)))

                        if not(b.devices.has_key(m) and (b.devices[m].name == module_name)):
                            d = Device(b, module_name, m)
                            d.add_functions(self._drivers_loaded[module_name])
                            b.add_device(m, d)

                            if module_name in self._openables:
                                b.add_openable_loaded(module_name)
                    else:
                        if b.devices.has_key(m):
                            b.devices.pop(m)

            except Exception, err:
                if self._debug:
                    print 'error module list', err

        return self._modules

    def _get_all_drivers(self):
        """
        Load the drivers for the differents devices
        """
        # current folder
        path_drivers = os.path.join(os.path.dirname(__file__), 'drivers')
        if self._debug:
            print 'Searching drivers in: ', path_drivers
        # normal drivers
        tmp = os.listdir(path_drivers)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._openables.append(name)
                self._get_driver(path_drivers, name)
        # hotplug drivers
        path = os.path.join(path_drivers, 'hotplug')
        tmp = os.listdir(path)
        tmp.sort()
        for d in tmp:
            if d.endswith('.py'):
                name = d.replace('.py', '')
                self._hotplug.append(name)
                self._get_driver(path, name)

    def _get_driver(self, path, driver):
        """
        Get a specify driver
        """
        if self._debug:
            print 'Loading driver %s...' % driver
        abs_path = os.path.abspath(os.path.join(path, driver + '.py'))
        f = None
        try:
            f = imp.load_source(driver, abs_path)
        except:
            if self._debug:
                print 'Cannot load %s' % driver, abs_path
        if f and hasattr(f, 'FUNCTIONS'):
            self._drivers_loaded[driver] = f.FUNCTIONS
        else:
            if self._debug:
                print 'Driver not have FUNCTIONS'

    def callModule(self, modulename, board_number, number, function, params = []):
        """
        Call one function: function for module: modulename in board: board_name
        with handler: number (only if the module is pnp, else, the parameter is
        None) with parameteres: params
        """
        try:
            board = self._bb[board_number]
            if board.devices.has_key(number) and (board.devices[number].name == modulename):
                return board.devices[number].call_function(function, params)
            else:
                if modulename in self._openables:
                    if modulename in board.get_openables_loaded():
                        number = board.get_device_handler(modulename)
                    else:
                        board.add_openable_loaded(modulename)
                        dev = Device(board, modulename)
                        number = dev.module_open()
                        dev.add_functions(self._drivers_loaded[modulename])
                        board.add_device(number, dev)
                    return board.devices[number].call_function(function, params)
                else:
                    if self._debug:
                        print 'no open and no openable'
                    return ERROR
        except Exception, err:
            if self._debug:
                print 'error call module', err
            return ERROR

    def reconnect(self):
        """
        Not implemented
        """
        pass

    def refresh(self):
        """
        Refresh: if no boards presents, search for them.. else, check if 
        the boards continues present
        """
        if self._bb == []:
            self.find_butias(False)
        else:
            for b in self._bb:
                info = ERROR
                try:
                    info = b.get_info()
                except:
                    if self._debug:
                        print 'error refresh getinfo'

                if info == ERROR:
                    self._bb.remove(b)
                    try:
                        b.close_baseboard()
                    except:
                        pass

    def close(self):
        """
        Closes all open baseboards
        """
        for b in self._bb:
            try:
                b.close_baseboard()
            except:
                if self._debug:
                    print 'error in close baseboard'
        self._bb = []

    def isPresent(self, module_name):
        """
        Check if module: module_name is present
        """
        module_list = self.get_modules_list()
        return (module_name in module_list)

    def loopBack(self, data, board=0):
        """
        LoopBack command: send data to the board and get the result. If all is ok
        the return must be exactly of the data parameter
        """
        return self.callModule('lback', board, 0, 'send', [data])

    ################################ Movement calls ################################

    def set2MotorSpeed(self, leftSense = 0, leftSpeed = 0, rightSense = 0, rightSpeed = 0, board = 0):
        """
        Set the speed of 2 motors. The sense is 0 or 1, and the speed is
        between 0 and 1023
        """
        msg = [int(leftSense), int(leftSpeed / 256.0), leftSpeed % 256, int(rightSense), int(rightSpeed / 256.0) , rightSpeed % 256]
        return self.callModule('motors', board, 0, 'setvel2mtr', msg)
     
    def setMotorSpeed(self, idMotor = 0, sense = 0, speed = 0, board = 0):
        """
        Set the speed of one motor. idMotor = 0 for left motor and 1 for the
        right motor. The sense is 0 or 1, and the speed is between 0 and 1023
        """
        msg = [idMotor, sense, int(speed / 256.0), speed % 256]
        return self.callModule('motors', board, 0, 'setvelmtr', msg)

    ############################### General calls ###############################
     
    def getBatteryCharge(self, board=0):
        """
        Gets the battery level charge
        """
        return self.callModule('butia', board, 0, 'get_volt')

    def getVersion(self, board=0):
        """
        Gets the version of Butiá module. 22 for new version
        """
        return self.callModule('butia', board, 0, 'read_ver')

    def getFirmwareVersion(self, board=0):
        """
        Gets the version of the Firmware
        """
        return self.callModule('admin', board, 0, 'getVersion')

    ############################### Sensors calls ###############################

    def getButton(self, number, board=0):
        """
        Gets the value of the button connected in port: number
        """
        res = self.callModule('button', board, number, 'getValue')
        if res != ERROR:
            return (1 - res)
        else:
            return res
    
    def getLight(self, number, board=0):
        """
        Gets the value of the light sensor connected in port: number
        """
        m = 65535
        res = self.callModule('light', board, number, 'getValue')
        if res != ERROR:
            return (m - res)
        else:
            return res

    def getDistance(self, number, board=0):
        """
        Gets the value of the distance sensor connected in port: number
        """
        return self.callModule('distanc', board, number, 'getValue')

    def getGray(self, number, board=0):
        """
        Gets the value of the gray sensor connected in port: number
        """
        return self.callModule('grey', board, number, 'getValue')

    def getTemperature(self, number, board=0):
        """
        Gets the value of the temperature sensor connected in port: number
        """
        return self.callModule('temp', board, number, 'getValue')

    def getResistance(self, number, board=0):
        """
        Gets the value of the resistance sensor connected in port: number
        """
        vcc = 65535
        raw = self.callModule('res', board, number, 'getValue')
        if not(raw == ERROR):
            return raw * 6800 / (vcc - raw)
        return raw

    def getVoltage(self, number, board=0):
        """
        Gets the value of the voltage sensor connected in port: number
        """
        vcc = 65535
        raw = self.callModule('volt', board, number, 'getValue')
        if not(raw == ERROR):
            return raw * 5 / vcc
        return raw

    def setLed(self, number, on_off, board=0):
        """
        Sets on or off the LED connected in port: number (0 is off, 1 is on)
        """
        return self.callModule('led', board, number, 'turn', [int(on_off)])

    ################################ Extras ################################

    def modeHack(self, pin, mode, board = 0):
        """
        Sets the mode of hack pin. If mode 0 = input, mode 1 = output
        """
        msg = [int(pin), int(mode)]
        return self.callModule('hackp', board, 0, 'setMode', msg)

    def setHack(self, pin, value, board = 0):
        """
        Sets the value of hack pin configured as output. Value is 0 or 1
        """
        msg = [int(pin), int(value)]
        return self.callModule('hackp', board, 0, 'write', msg)

    def getHack(self, pin, board = 0):
        """
        Gets the value of hack pin configured as input. Returns 0 or 1
        """
        return self.callModule('hackp', board, 0, 'read', [int(pin)])

