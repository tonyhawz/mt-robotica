from pybot import usb4butia
import motores
import time
import threading
from motoresPinza import MotoresPinza
lbutia = usb4butia.USB4Butia()
l = threading.Lock()
mov = motores.Motores(lbutia,l)

motorPinza = MotoresPinza(lbutia, l)

#motorPinza.abierta()
#time.sleep(2)

#motorPinza.aCargar()
#time.sleep(3)
#motorPinza.cargar()
#time.sleep(2)
#motorPinza.abierta()
#time.sleep(3)

motorPinza.setPosition(5, 200)
motorPinza.setPosition(7, 811)
time.sleep(2)

mov.descargarTolva()
time.sleep(2)
#motorPinza.abierta()
motorPinza.setPosition(5, 0)
motorPinza.setPosition(7, 1023)
#time.sleep(2)

#mov.posicion_levantar()

#while True:
    #print lbutia.getDistance(1)


#mov.avanzar_u(400)
#mov.girar_antihorario()
#time.sleep(4)
#mov.retroceder_u(400)
#time.sleep(3)
#mov.girar_antihorario()
#mov.girar_antihorario()
#mov.girar_antihorario()
#mov.girar_antihorario()
#mov.girar_antihorario()

#time.sleep(2)

#mov.avanzar_u(400)
#time.sleep(2)
mov.detener()

'''
mov.avanzar_u(400)
#time.sleep(4)
#mov.retroceder_u(400)
#time.sleep(4)
#mov.girar_antihorario()
time.sleep(2)
#mov.avanzar_u(400)
#time.sleep(4)
mov.girar_horario()
time.sleep(6)
#mov.avanzar_u(400)
#time.sleep(5)
mov.detener()

mov.centrarCamara()
time.sleep(3)
print (mov.get_posicion_camara() )
mov.hacerPaneoCamara()
time.sleep(5)
print (mov.get_posicion_camara() )
mov.hacerPaneoCamara()
time.sleep(5)
print (mov.get_posicion_camara() )
#mov.girar_marchatras_viejo(True)
print (mov.get_posicion_camara() )


mov.girarCamaraIzquierda()
time.sleep(1)
mov.girarCamaraIzquierda()
time.sleep(1)
mov.girarCamaraIzquierda()
time.sleep(1)
mov.girarCamaraIzquierda()
time.sleep(1)
mov.girarCamaraIzquierda()

mov.girarCamaraDerecha()
time.sleep(1)
mov.girarCamaraDerecha()
time.sleep(1)
mov.girarCamaraDerecha()
time.sleep(1)
mov.girarCamaraDerecha()
time.sleep(1)
mov.girarCamaraDerecha()'''
