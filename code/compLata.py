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
       #if (self.data.read('SensorCamPos::pos_x')== config.cero_posx_camara and self.data.read('SensorCamPos::pos_y')== 0):
            if ((self.data.read('Camara::lata_x') > config.min_x) and (self.data.read('Camara::lata_x') < config.max_x)):
                self.motores.avanzar_u(config.VEL)
                print ("AREA LATA " + str(self.data.read('Camara::area')))
                if (self.data.read('Camara::area') > config.area_lata)  and self.data.read('Camara::lata_y') > config.min_y:
                    self.data.write('lata::disponible', 1)
                    self.motores.detener()
                    print "EEEEEENNNNNNNNNNNCCCCCCCCCCCCCOOOOONNNNNNNNNNNNTREEEEEEEEEEEEEEEEEE"
            elif (self.data.read('Camara::lata_x') < config.min_x):
                print "izquierda"
                self.motores.girar_lugar_antihorario()
            elif (self.data.read('Camara::lata_x') > config.max_x):
                print "derecha"
                self.motores.girar_lugar_horario()
        #else:
            ##Si la camara no esta centrada hay que ajustar camara y robot
            #if (self.data.read('SensorCamPos::pos_x') < config.cero_posx_camara and self.data.read('Camara::lata_x') < config.min_x):
                ##camara girada a la derecha y lata a la izquierda de la camara solo giro la camara
                #self.motores.girarCamaraIzquierda()
                #self.motores.avanzar_u(config.VEL)
            #elif (self.data.read('SensorCamPos::pos_x') < config.cero_posx_camara and  self.data.read('Camara::lata_x') > config.max_x):
                #print "giro derecha"
                #self.motores.girar_horario()
            #elif (self.data.read('SensorCamPos::pos_x') > config.cero_posx_camara and self.data.read('Camara::lata_x') < config.min_x):
                ##camara girada a la izquierda  y lata a la izquierda de la camara solo giro la camara
                #self.motores.girarCamaraIzquierda()
                #self.motores.girar_antihorario()
            #elif (self.data.read('SensorCamPos::pos_x')> config.cero_posx_camara and  self.data.read('Camara::lata_x') > config.max_x):
                #print "giro derecha"
                #self.motores.girarCamaraDerecha()
                #self.motores.avanzar_u(config.VEL)


    '''
    def action(self):
        print 'CompLata::action'
        #Si la camara esta centrada es como antes
        #if (self.data.read('SensorCamPos::pos_x')== config.cero_posx_camara and self.data.read('SensorCamPos::pos_y')== 0):
        #if self.data.read('SensorCamPos::pos_y') is 0:
        #    if ((self.data.read('Camara::lata_x') > config.min_x) and (self.data.read('Camara::lata_x') < config.max_x)):
        #        self.motores.avanzar_u(config.VEL)
                #if (self.data.read('Camara::area') > config.area_lata):
                #    self.data.write('lata::disponible', 1)
                #    self.motores.detener()
                #    print "EEEEEENNNNNNNNNNNCCCCCCCCCCCCCOOOOONNNNNNNNNNNNTREEEEEEEEEEEEEEEEEE"
        #    elif (self.data.read('Camara::lata_x') < config.min_x):
                #self.motores.girar_antihorario()
        #        print "izquierda"
        #        self.motores.girar_antihorario()
        #    elif (self.data.read('Camara::lata_x') > config.max_x):
        #        print "derecha"
        #        self.motores.girar_horario()
        #else:
            #Si la camara no esta centrada hay que ajustar camara y robot
            #if (self.data.read('SensorCamPos::pos_x')< 0 and
            #if ( self.data.read('Camara::lata_x') < config.min_x):
                #camara girada a la derecha y lata a la izquierda de la camara solo giro la camara
                #self.motores.girar_camara_izquierda()
            #    self.motores.avanzar_u(config.VEL)
            #elif (#self.data.read('SensorCamPos::pos_x')< 0 and
        if( self.data.read('Camara::lata_x') > config.max_x):
            #camara girada a la derecha y lata a la derecha de la camara solo giro el robot
            print "derecha"
            self.motores.girar_horario()
            #elif (#self.data.read('SensorCamPos::pos_x')> 0 and
            #elif ( self.data.read('Camara::lata_x') > config.max_x):
                #self.motores.girar_camara_derecha()
            #   self.motores.avanzar_u(config.VEL)
            #elif (#self.data.read('SensorCamPos::pos_x')> 0 and
        elif( self.data.read('Camara::lata_x') < config.min_x):
            print "izquierda"
            self.motores.girar_antihorario()
            #@TODO VER QUE PASA CON LAS Y EN LA CAMARA
    '''

    def reset(self):
        self.data.write('Camara::area', 0)
        self.data.write('Camara::lata_x', 0)
        self.data.write('Camara::encontro', 'FALSE')
        self.data.write('lata::disponible', 0)

    def post_stop(self):
        print 'CompLata::post_stop'

    def getTime(self):
        return time.time()


