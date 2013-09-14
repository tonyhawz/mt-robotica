'''
Created on May 7, 2013

@author: matias
'''

import time
from Communication import CommSerial
import Actuator

comm_tty = CommSerial() 
comm_tty.connect()
actuator = Actuator.Actuator(comm_tty)
motor_id = 3

actuator.reset(motor_id)
time.sleep(2)
actuator.setear_id(motor_id)

for i in range(1, 50):
    if (i%2 == 0):
        actuator.led_state_change(motor_id, 1)
    else:
        actuator.led_state_change(motor_id, 0)
    time.sleep(.1)
#
