#! /usr/bin/env python
# -*- coding: utf-8 -*-
from Communication import CommSerial
import Actuator

comm_tty = CommSerial()  #TODO read a configuration file to use the correct parameters for CommSimulator
comm_tty.connect()
actuator_tty = Actuator.Actuator(comm_tty)

motor_id = 8

actuator_tty.set_AngleLimit(motor_id, 0 , 1023)
#actuator_tty.move_actuator(motor_id, 0xAA,0xAA)
actuator_tty.move_actuator(motor_id, 511,200)

