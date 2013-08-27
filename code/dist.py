from pybot import usb4butia
import time

# inicializo
butia = usb4butia.USB4Butia()

# imprimo distancia
while True:
    butia.refresh()
    dist = butia.getDistance(2)
    dist1 = butia.getDistance(5)
    dist2 = butia.getDistance(6)
    print(dist)
    print(dist1)
    print(dist2)
    time.sleep(1)
