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
from Communication import CommSerial
import Actuator

#comm = CommSimulator()  #TODO read a configuration file to use the correct parameters for CommSimulator
comm_tty = CommSerial()  #TODO read a configuration file to use the correct parameters for CommSimulator
#comm.connect()
comm_tty.connect()
#actuator = Actuator.Actuator(comm)
actuator_tty = Actuator.Actuator(comm_tty)
#actuator_tty.setear_id(6)
idMotor = 6

#actuator_tty.move_actuator(6, 0 , 32)
#actuator_tty.set_speed_actuator(motor_id, 256, 0)

actuator_tty.setTorque(idMotor, True)

#actuator_tty.move_actuator(idMotor, 0, 120)
