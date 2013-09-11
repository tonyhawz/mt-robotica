from pybot import usb4butia

print ("aca")
lbutia = usb4butia.USB4Butia(True)
print ("aca")
lbutia.refresh()
lbutia.module_open('ax')
print (lbutia.getModulesList())

print ("hola")