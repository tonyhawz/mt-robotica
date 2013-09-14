# -*- coding: utf-8 -*-
import sys
import time

sys.path.append("../code/")

from myUsb4Butia import MyUsb4Butia

T_SLEEP = 0.5


class PinzaTest():

    def __init__(self):
        #super(PinzaTest, self).__init__()
        self.b = MyUsb4Butia()
        self.speed = 200

    def initMotors(self):
        self.initMotorPinza(5)
        self.initMotorPinza(6)
        self.initMotorPinza(7)
        self.initMotorPinza(8)

    def initMotorPinza(self, motor_id):
        self.b.jointMode(motor_id, 0, 1023)
        self.b.setSpeed(motor_id, self.speed)

    def setSpeed(self, speed):
        self.speed = speed

    def setPosition(self, motor_id, pos, speed=None):
        self.b.jointMode(motor_id, 0, 1023)
        if speed is None:
            self.b.setSpeed(motor_id, speed)
        else:
            self.b.setSpeed(motor_id, self.speed)
        self.b.setPosition(motor_id, pos)

    def abierta(self):
        self.setPosition(5, 0)
        self.setPosition(7, 1023)
        self.setPosition(8, 750)
        self.setPosition(6, 280)

    def aCargar(self):
        self.setPosition(5, 200)
        self.setPosition(7, 811)
        self.setPosition(8, 511)
        self.setPosition(6, 511)


def main(argv):
    m = PinzaTest()
    m.initMotors()
    m.setSpeed(200)

    m.abierta()

    #print "moviendo pinza izq"
    #m.setPosition(8, 511)
    #time.sleep(T_SLEEP)
    #print "moviendo pinza der"
    #m.setPosition(6, 511)
    #time.sleep(T_SLEEP)
    #print "moviendo pinza izq"
    #m.setPosition(5, 511)
    #time.sleep(T_SLEEP)
    #print "moviendo pinza der"
    #m.setPosition(7, 511)

    #time.sleep(2)
    ## posicionandose para navegar
    #time.sleep(T_SLEEP)
    #m.setPosition(5, 0)
    #time.sleep(T_SLEEP)
    #m.setPosition(7, 1023)

    #time.sleep(T_SLEEP)
    #m.setPosition(8, 311)
    #time.sleep(T_SLEEP)
    #m.setPosition(6, 700)


if __name__ == "__main__":
    main(sys.argv[:])

