from pybot import usb4butia
import motores
import time
import threading

lbutia = usb4butia.USB4Butia()
l = threading.Lock()
mov = motores.Motores(lbutia,l)

mov.descargarTolva()

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
