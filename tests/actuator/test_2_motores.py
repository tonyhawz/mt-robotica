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

from Communication import CommSerial
from Actuator import Actuator

comm_tty = CommSerial()  #TODO read a configuration file to use the correct parameters for CommSimulator
comm_tty.connect()
actuator_tty = Actuator(comm_tty)

motorI = 6
motorD = 12

actuator_tty.mover_2_motoresA(motorI, motorD, 500, 1, 2.5, 20, 0.4)

