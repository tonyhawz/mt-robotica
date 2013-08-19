from pybot import usb4butia
import motores
import time
import threading

lbutia = usb4butia.USB4Butia()
l = threading.Lock()
mov = motores.Motores(lbutia,l)

mov.girar_antihorario()
time.sleep(1)
mov.detener()


