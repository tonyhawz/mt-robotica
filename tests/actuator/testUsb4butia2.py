'''

Created on May 7, 2013

@author: matias

'''
import sys
import time
from pybot import usb4butia

u = usb4butia.USB4Butia()

modules = u.get_modules_list()
for val in modules:
    print (val)

print u.getFirmwareVersion()
drivers = u._get_all_drivers()
print drivers

u.set2MotorSpeed(6, 256, 12, 256)

time.sleep(5)

u.set2MotorSpeed(6, 0, 12, 0)
