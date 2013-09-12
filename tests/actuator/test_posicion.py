#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 
# basic ax12 actuator control
# Andrés Aguirre Dorelo
# MINA/INCO/UDELAR
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

import time
import Communication
from Communication import CommSimulator
from Communication import CommSerial
import Actuator
from compiler.ast import Print

#comm = CommSimulator()  #TODO read a configuration file to use the correct parameters for CommSimulator
comm_tty = CommSerial()  #TODO read a configuration file to use the correct parameters for CommSimulator
#comm.connect()
comm_tty.connect()
#actuator = Actuator.Actuator(comm)
actuator_tty = Actuator.Actuator(comm_tty)

motor_id = 6

print "actuator_tty.set_AngleLimit(motor_id, 0x0000, 0x0000)"
actuator_tty.set_AngleLimit(motor_id, 0x0000, 0x0000)
time.sleep(1)


print "actuator_tty.setTorque(motor_id, False)"
actuator_tty.setTorque(motor_id, False)
time.sleep(1)

print "actuator_tty.set_speed_actuator(motor_id, 0x200, 0x0)"
actuator_tty.set_speed_actuator(motor_id, 0x200, 0x0)
time.sleep(1)

print "actuator_tty.setTorqueMaximo(motor_id,500)"
actuator_tty.setTorqueMaximo(motor_id,500)
time.sleep(1)

print "actuator_tty.setTorque(motor_id, True)"
actuator_tty.setTorque(motor_id, True)
time.sleep(1) 

print "."
time.sleep(1) 
print "."
time.sleep(1) 
print "."
time.sleep(1) 
print "."
actuator_tty.setTorque(motor_id, False)


#actuator_tty.move_actuator(motor_id, 150, 200)

#actuator_tty.led_state_change(motor_id, 1)
#  else: 
#actuator.set_speed_actuator(motor_id, 20)
#actuator.move_actuator(motor_id, 0x0000, 0x0500)
#actuator_tty.move_actuator(motor_id, 0x0000, 0x0500)
#actuator_tty.led_state_change(motor_id, 0)
#time.sleep(.5)

