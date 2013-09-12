import comp
import time
import config
import random


class CompWander(comp.Comp):

    timeout = None
    t_antes = None
    estado = 1
    ADELANTE = 0
    GIRAR_D = 1
    GIRAR_I = 2
    VEL = None

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.timeout = config.motores_timeout_adelante
        self.motores = motores
        self.estado = self.ADELANTE
        self.t_antes = self.getTime()
        self.VEL = config.VEL

    def getNombre(self):
        return 'CompWander'

    def takeControl(self):
        return True

    def action(self):
        self.printStatus()
        delta_t = self.getTime() - self.t_antes
        self.timeout = self.timeout - delta_t
        self.t_antes = self.getTime()

        if (self.timeout < 0):
            if (self.estado is self.ADELANTE):
                self.estado = random.randint(1, 2)
                self.timeout = config.motores_timeout_girar
            else:
                self.estado = self.ADELANTE
                self.timeout = config.motores_timeout_adelante

        if (self.estado is self.ADELANTE):
            self.motores.avanzar_u(self.VEL)
        elif self.estado is self.GIRAR_D:
            self.motores.girar_horario()
        elif self.estado is self.GIRAR_I:
            self.motores.girar_antihorario()
        #self.motores.hacerPaneoCamara()

    def reset(self):
        pass

    def post_stop(self):
        print('CompWander::post_stop')
        self.timeout = config.motores_timeout_adelante
        self.estado = self.ADELANTE

    def getTime(self):
        return time.time()

    def printStatus(self):
        s = 'UNKNOWN STATUS'
        if self.estado is self.ADELANTE:
            s = 'ADELANTE'
        elif self.estado is self.GIRAR_D:
            s = 'GIRAR_D'
        elif self.estado is self.GIRAR_I:
            s = 'GIRAR_I'
        print('CompWander::action  ' + s + ' ' + str(self.timeout))