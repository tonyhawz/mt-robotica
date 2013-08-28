import time
import signal
import sys
import config
import threading

from comp import Comp
from arbitro import Arbitro 
#from arbitro_st import ArbitroST 
from data import Data 
from sensor import Sensor 
from compEvitar import CompEvitar
from compWander import CompWander
from compAlfombra import CompAlfombra
from compLata import CompLata
from compBoton import CompBoton
from compCargarLata import CompCargarLata
from pybot import usb4butia
from sensorGrises import SensorGrises 
from sensorDistancia import SensorDistancia 
from sensorBoton import SensorBoton 
from sensorCameraWhite import SensorCameraWhite
from motores import Motores 

global hilos
global lock_u4b

lock_u4b = threading.Lock()
u4b = usb4butia.USB4Butia()
motor = Motores(u4b, lock_u4b) 


hilos = []

print 'Press Ctrl+C'

data = Data() 


#  CompBoton(data, motor), 

comportamientos  = [ CompAlfombra(data, motor), CompEvitar(data, motor), CompCargarLata(data, motor), CompLata(data, motor, lock_u4b),  CompWander(data, motor)]

a = Arbitro(comportamientos,data) 
a.start()

#sensores = [Sensor(data), SensorDistancia(data, u4b, 1, lock_u4b), SensorGrises(data, u4b, 1, lock_u4b), SensorGrises(data,u4b,3,lock_u4b),SensorCameraWhite(data,lock_u4b)]


#sensores = [SensorGrises(data, u4b, config.grisDer, lock_u4b), SensorGrises(data,u4b,config.grisIzq,lock_u4b),SensorCameraWhite(data,lock_u4b)]

sensores = [Sensor(data),  SensorGrises(data, u4b, config.grisDer, lock_u4b), SensorGrises(data,u4b,config.grisIzq,lock_u4b)]



hilos.append(a)
hilos.append(motor)

for s in sensores:
    s.start()
    hilos.append(s) 

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    for h in hilos:
        h.stop()
        print 'PARANDO ' + h.getNombre()
#    motor.detener()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

signal.pause()

