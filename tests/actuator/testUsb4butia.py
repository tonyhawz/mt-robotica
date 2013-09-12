'''

Created on May 7, 2013

@author: matias

'''
import sys
import time
from pybot.usb4butia import USB4Butia
from pybot import usb4butia

u = usb4butia.USB4Butia()

modules = u.get_modules_list()

while True:
    print u.getDistance(5)
    time.sleep(1)    
