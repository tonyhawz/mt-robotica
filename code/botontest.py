from pybot import usb4butia

u4b = usb4butia.USB4Butia()

while True:
    bot = u4b.getButton(6)
    print bot


