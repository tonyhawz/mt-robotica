import comp
import time
import config

class CompBoton(comp.Comp):

    parado = True
    arbitro = None
    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.key = 'SensorBoton::' + str(config.idBoton)
        self.data.write(self.key, -1)
        self.motores = motores


    def setArbitro(self, arbitro):
        self.arbitro = arbitro

    def takeControl(self):
        if self.data.read('SensorBoton::' + str(config.idBoton)) == 0:
            self.parado = not self.parado
        return self.parado
        #print str(self.data.read('SensorBoton::' + str(config.idBoton))) + "en comp"
        #return self.data.read('SensorBoton::' + str(config.idBoton)) == 1

    def action(self):
        print "PARANDO"
        self.motores.detener()
        #time.sleep(1)
        '''if( self.arbitro != None):
            self.motores.detener()
            if self.parado:
                self.arbitro.arbitrar()
                self.parado=True
                print "mando ARRANCAR!!!!"
            else:
                self.arbitro.stop()
                self.motores.detener()
                self.parado= False
                print "mando PARARR!!!!"'''

    #def run(self):
        #self.stop = False
        #while not self.stop:
            #if self.data.read('SensorBoton::' + str(config.idBoton)) == 0:
                #if self.parado:
                    #self.arbitro.resume()
                    #self.parado=False
                    #print "mando ARRANCAR!!!!"
                #else:
                    #self.arbitro.pause()
                    #self.motores.detener()
                    #self.parado= True
                    #print "mando PARARR!!!!"
            #time.sleep(1)

    def getNombre(self):
        return 'CompBoton'


    def reset(self):
        pass

    def post_stop(self):
        pass

    def stop(self):
        self.stop = True
