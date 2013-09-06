import comp 
import time
import config

class CompLata(comp.Comp):

    def __init__(self, data, motores, lock_u4b):
        comp.Comp.__init__(self, data)
        self.motores = motores
        self.data.write('Camara::area', 0)
        self.data.write('Camara::lata_x', 0)
        self.data.write('Camara::encontro', 'FALSE')
        self.data.write('lata::disponible', 0)

    def getNombre(self):
        return 'CompLata'

    def takeControl(self):
        #val = self.data.read('Camara::area')
	#print "area= " + str(val)
        #return (val > config.min_area) and (self.data.read('lata::disponible') == 0)
	return self.data.read('Camara::encontro') == 'TRUE'

    def action(self):
        print 'CompLata::action'

        if ((self.data.read('Camara::lata_x') > config.min_x) and (self.data.read('Camara::lata_x') < config.max_x)):
            self.motores.avanzar_u(config.VEL)
            if (self.data.read('Camara::area') > config.area_lata):
                self.data.write('lata::disponible', 1)
                self.motores.detener()
                print "EEEEEENNNNNNNNNNNCCCCCCCCCCCCCOOOOONNNNNNNNNNNNTREEEEEEEEEEEEEEEEEE"
        elif (self.data.read('Camara::lata_x') < config.min_x):
            #self.motores.girar_antihorario()
            print "izquierda"
            self.motores.girar_antihorario()
        elif (self.data.read('Camara::lata_x') > config.max_x):
            print "derecha"
            self.motores.girar_horario()

    def reset(self):
        self.data.write('Camara::area', 0)
        self.data.write('Camara::lata_x', 0)
	self.data.write('Camara::encontro', 'FALSE')
        self.data.write('lata::disponible', 0)

    def post_stop(self):
        print 'CompLata::post_stop'
        
    def getTime(self):
        return time.time()


