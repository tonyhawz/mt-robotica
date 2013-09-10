# -*- coding: utf-8 -*-
import sys
import time

sys.path.append("../code/")

from myUsb4Butia import MyUsb4Butia


class PinzaTest():

    def __init__(self):
        #super(PinzaTest, self).__init__()
        self.b = MyUsb4Butia()

    def initMotors(self):
        self.initMotorPinza(5)
        self.initMotorPinza(6)
        self.initMotorPinza(7)
        self.initMotorPinza(8)

    def initMotorPinza(self, motor_id):
        self.b.jointMode(motor_id, 0, 1023)
        self.b.setSpeed(motor_id, 200)


def main(argv):
    m = PinzaTest()
    m.initMotors()
    print "moviendo pinza izq"
    m.b.setPosition(8, 511)
    time.sleep(1)
    print "moviendo pinza der"
    m.b.setPosition(6, 511)
    time.sleep(1)
    print "moviendo pinza izq"
    m.b.setPosition(5, 511)
    time.sleep(1)
    print "moviendo pinza der"
    m.b.setPosition(7, 511)


if __name__ == "__main__":
    main(sys.argv[:])

