# -*- coding: utf-8 -*-

from pybot.usb4butia import USB4Butia

ERROR = -1


class MyUsb4Butia(USB4Butia):

    def __init__(self):
        super(MyUsb4Butia, self).__init__()

    ############################## Movement calls #############################

    def set2MotorSpeed(self, leftSense=0, leftSpeed=0, rightSense=0,
    rightSpeed=0, board=0):
        """
        Set the speed of 2 motors. The sense is 0 or 1, and the speed is
        between 0 and 1023
        """
        msg = [int(leftSense), int(leftSpeed / 256.0), leftSpeed % 256,
        int(rightSense), int(rightSpeed / 256.0), rightSpeed % 256]
        return self.callModule('motors', board, 0, 'setvel2mtr', msg)

    def setMotorSpeed(self, idMotor=0, sense=0, speed=0, board=0):
        """
        Set the speed of one motor. idMotor = 0 for left motor and 1 for the
        right motor. The sense is 0 or 1, and the speed is between 0 and 1023
        """
        msg = [idMotor, sense, int(speed / 256.0), speed % 256]
        return self.callModule('motors', board, 0, 'setvelmtr', msg)

    ############################### General calls #############################

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

    ############################### Sensors calls #############################

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

    ################################# Extras ##################################

    def modeHack(self, pin, mode, board=0):
        """
        Sets the mode of hack pin. If mode 0 = input, mode 1 = output
        """
        msg = [int(pin), int(mode)]
        return self.callModule('hackp', board, 0, 'setMode', msg)

    def setHack(self, pin, value, board=0):
        """
        Sets the value of hack pin configured as output. Value is 0 or 1
        """
        msg = [int(pin), int(value)]
        return self.callModule('hackp', board, 0, 'write', msg)

    def getHack(self, pin, board=0):
        """
        Gets the value of hack pin configured as input. Returns 0 or 1
        """
        return self.callModule('hackp', board, 0, 'read', [int(pin)])