#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Communication import CommSerial
import Actuator
import time

comm_tty = CommSerial()  #TODO read a configuration file to use the correct parameters for CommSimulator
comm_tty.connect()
actuator_tty = Actuator.Actuator(comm_tty)

motorD = 1

actuator_tty.set_AngleLimit(motorD, 0, 0)

print "actuator_tty.set_speed_actuator(motor_id, 0x200, 0x0)"
actuator_tty.set_speed_actuator(motorD, 200, 0)

time.sleep(1)

actuator_tty.set_speed_actuator(motorD, 0x0, 0x0)

