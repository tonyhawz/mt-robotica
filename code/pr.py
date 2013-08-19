from pybot import usb4butia
import motores
import time
import threading

lbutia = usb4butia.USB4Butia()
l = threading.Lock()
mov = motores.Motores(lbutia,l)

#mov.refresh()
#mov.girar_marchatras(True)
#mov.girar_marchatras(True)
#time.sleep(2)
#mov.avanzar_u(800)
#time.sleep(2)
mov.detener()


