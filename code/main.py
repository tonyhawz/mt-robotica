#import time
import signal
import sys
import config
import threading

#from comp import Comp
from arbitro import Arbitro
#from arbitro_st import ArbitroST
from data import Data
#from sensor import Sensor
from compEvitar import CompEvitar
from compWander import CompWander
#from compAlfombra import CompAlfombra
from compLona import CompLona
from compLata import CompLata
#from compBoton import CompBoton
from compCargarLata import CompCargarLata
#from pybot import usb4butia
from sensorDistancia import SensorDistancia
#from sensorBoton import SensorBoton
from sensorCameraWhite import SensorCameraWhite
from motores import Motores
from myUsb4Butia import MyUsb4Butia
from motoresPinza import MotoresPinza
#from sensorCamaraPos import SensorCamaraPos

global hilos
global lock_u4b

lock_u4b = threading.Lock()
u4b = MyUsb4Butia()
motor = Motores(u4b, lock_u4b)
motorPinza = MotoresPinza(u4b, lock_u4b)
hilos = []

print ('Press Ctrl+C')

data = Data()


#comboton = CompBoton(data, motor)
#los compportamientos van en orden descendente deprioridad
comportamientos = [
    #comboton,
    #CompAlfombra(data, motor),
    #CompLona(data, motor),
    CompEvitar(data, motor),
    CompCargarLata(data, motorPinza,motor),
    CompLata(data, motor, lock_u4b),
    CompWander(data, motor)
    ]

a = Arbitro(comportamientos, data,u4b)
a.start()
#comboton.setArbitro(a)
#comboton.start()


#sensores = [Sensor(data),
#    SeqnsorDistancia(data, u4b, 1, lock_u4b),
#    SensorGrises(data, u4b, 1, lock_u4b),
#    SensorGrises(data,u4b,3,lock_u4b),
#    SensorCameraWhite(data,lock_u4b)]


#sensores = [SensorGrises(data, u4b, config.grisDer, lock_u4b),
#    SensorGrises(data,u4b,config.grisIzq,lock_u4b),
#    SensorCameraWhite(data, lock_u4b)]

sensores = [
    SensorDistancia(data, u4b, 1, lock_u4b),
    #SensorBoton(data, u4b, lock_u4b)
    SensorCameraWhite(data, lock_u4b),
    #SensorCamaraPos(data,motor, lock_u4b)
    #Sensor(data),
    #SensorGrises(data, u4b, config.grisDer, lock_u4b),
    #SensorGrises(data, u4b, config.grisIzq, lock_u4b)
    ]

hilos.append(a)
hilos.append(motor)
#hilos.append(comboton)

for s in sensores:
    s.start()
    hilos.append(s)


def signal_handler(signal, frame):
    print ('You pressed Ctrl+C!')
    for h in hilos:
        msg = 'PARANDO ' + h.getNombre()
        print (msg)
        h.stop()
    #motor.detener()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

signal.pause()

