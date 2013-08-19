from pybot import usb4butia
import time

butia = usb4butia.USB4Butia()
modules = butia.get_modules_list()

# listado de componentes presentes...
for v in modules:
    print str(v)

print str(butia.getButton(6, 0))
