import comp
#import time
import config
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

    def action(self):
        print 'CompBuscarTacho::action'
        if ((self.data.read('Camara::tacho_x') > config.min_x) and (self.data.read('Camara::tacho_x') < config.max_x)):
            self.motores.avanzar_u(config.VEL)
            #VER CUANDO PARA
            if (self.data.read('Camara::area') > config.area_lata):
                self.motores.detener()
                self.data.write('Tacho::disponible', 1)
                print "Frente al TACHO"
        elif (self.data.read('Camara::tacho_x') < config.min_x):
            #self.motores.girar_antihorario()
            print "izquierda"
            self.motores.girar_antihorario()
        elif (self.data.read('Camara::tacho_x') > config.max_x):
            print "derecha"
            self.motores.girar_horario()


    def reset(self):
        pass


