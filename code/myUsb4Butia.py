# -*- coding: utf-8 -*-

from pybot.usb4butia import USB4Butia

ERROR = -1


class MyUsb4Butia(USB4Butia):

    def __init__(self):
        USB4Butia.__init__(self)

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

    ################################# Extras ##################################

    def writeInfo(self, motor_id, regstart, value, board=0):
        msg = [motor_id, regstart, value]
        return self.callModule('ax', board, 0, 'writeInfo', msg)

    def wheelMode(self, motor_id, board=0):
        msg = [motor_id]
        return self.callModule('ax', board, 0, 'wheelMode', msg)

    def readInfo(self, motor_id, regstart, lenght, board=0):
        msg = [motor_id, regstart, lenght]
        return self.callModule('ax', board, 0, 'readInfo', msg)

    def setSpeed(self, motor_id, speed, board=0):
        msg = [motor_id, speed]
        return self.callModule('ax', board, 0, 'setSpeed', msg)

    def sendPacket(self, motor_id, pack, board=0):
        msg = [motor_id, pack]
        return self.callModule('ax', board, 0, 'sendPacket', msg)

    def getVersionAx(self, board=0):
        msg = []
        return self.callModule('ax', board, 0, 'getVersion', msg)

    def jointMode(self, motor_id, _min, _max, board=0):
        msg = [motor_id, _min, _max]
        return self.callModule('ax', board, 0, 'jointMode', msg)

    def setPosition(self, motor_id, pos, board=0):
        msg = [motor_id, pos]
        return self.callModule('ax', board, 0, 'setPosition', msg)

    def getPosition(self, motor_id, board=0):
        msg = [motor_id]
        return self.callModule('ax', board, 0, 'getPosition', msg)


def main():
    m = MyUsb4Butia()
    print ("firmware " + str(m.getFirmwareVersion()))
    print m.getModulesList()
    print "version " + str(m.callModule('ax', 0, 0, 'getVersion', []))
    print(m.getPosition(5))

if __name__ == "__main__":
    main()