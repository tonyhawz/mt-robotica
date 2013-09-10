import comp
import time

class CompDescargarLatas(comp.Comp):


	def __init__(self, data, motores):
		comp.Comp.__init__(self, data)
		self.motores = motores

	def takeControl(self):
		return self.data.read('Tacho::disponible') ==1

	def action(self):
	    print 'CompDescargarLatas::action'
	    #DEBERIA DE HACER UN GIRO DE 180 y tirar las latas
	    # Se podria girar 180 hasta que un sensor de distacias atas diga q hay algo atras
	    # ver de poner sensores adelante del tacho para el tema de las distancias		