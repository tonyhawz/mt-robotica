import comp
import time

class CompBuscarTacho(comp.Comp):


	def __init__(self, data, motores):
		comp.Comp.__init__(self, data)
		self.motores = motores

	#Tomo el control solo si tengo el tacho en frente y tengo latas
	#@TODO comportamiento con respecto a latas y tacho
	def takeControl(self):
	 	if (self.data.read('Camara::tacho')=='TRUE'):
	 		return self.data.read('lata::cant_latas')>0
		else:
			return False

	#def action(self):
	#	self.data.read('Camara::tacho_x', x)
    #    self.data.read('Camara::tacho_y', y)

	def action(self):
	    print 'CompBuscarTacho::action'
	    #Si la camara esta centrada es como antes
	    if (self.data.read('SensorCamPos::pos_x')== 0 and self.data.read('SensorCamPos::pos_y')== 0):
	        if ((self.data.read('Camara::tacho_x') > config.min_x) and (self.data.read('Camara::tacho_x') < config.max_x)):
	            self.motores.avanzar_u(config.VEL)
	            #VER CUANDO PARA 
	            #if (self.data.read('Camara::area') > config.area_lata):
	            #	self.motores.detener()
                # 	self.data.write('Tacho::disponible', 1)
	            #    print "Frente al TACHO"
	        elif (self.data.read('Camara::tacho_x') < config.min_x):
	            #self.motores.girar_antihorario()
	            print "izquierda"
	            self.motores.girar_antihorario()
	        elif (self.data.read('Camara::tacho_x') > config.max_x):
	            print "derecha"
	            self.motores.girar_horario()
	    else:
	        #Si la camara no esta centrada hay que ajustar camara y robot
	        if (self.data.read('SensorCamPos::pos_x')< 0 and self.data.read('Camara::tacho_x') < config.min_x):
	            #camara girada a la derecha y lata a la izquierda de la camara solo giro la camara
	            self.motores.girar_camara_izquierda()
	            self.motores.avanzar_u(config.VEL)
	        elif (self.data.read('SensorCamPos::pos_x')< 0 and self.data.read('Camara::tacho_x') > config.max_x):
	            #camara girada a la derecha y lata a la derecha de la camara solo giro el robot               
	            print "derecha"
	            self.motores.girar_horario()
	        elif (self.data.read('SensorCamPos::pos_x')> 0 and self.data.read('Camara::tacho_x') > config.max_x):
	            self.motores.girar_camara_derecha()
	            self.motores.avanzar_u(config.VEL)
	        elif (self.data.read('SensorCamPos::pos_x')> 0 and self.data.read('Camara::tacho_x') < config.min_x):
	            print "izquierda"
	            self.motores.girar_antihorario()
	        #@TODO VER QUE PASA CON LAS Y EN LA CAMARA



 	def reset(self):
 		pass


