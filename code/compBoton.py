import comp 
import time
import config

class CompBoton(comp.Comp):

    parado = True

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.key = 'SensorBoton::' + str(config.idBoton)
        self.data.write(self.key, 0)
        self.motores = motores

    def takeControl(self):
        if self.data.read('SensorBoton::' + str(config.idBoton)) == 1:
            self.parado = not self.parado 
        return self.parado

    def action(self):
        self.motores.detener()


    def reset(self):
        pass

    def post_stop(self):
        pass

