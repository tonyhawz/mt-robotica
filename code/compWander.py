import comp
import time

TIMEOUT = 10000


class CompWander(comp.Comp):

    timeout = None
    t_antes = None
    estado = 1
    ADELANTE = 0
    GIRAR_D = 1
    GIRAR_I = 2
    VEL = 400

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.timeout = TIMEOUT
        self.motores = motores
        self.estado = self.ADELANTE
        self.t_antes = self.getTime()

    def getNombre(self):
        return 'CompWander'

    def takeControl(self):
        return True

    def action(self):
        print('CompWander::action')
        deltaT = self.getTime() - self.t_antes
        self.timeout = self.timeout - deltaT
        self.t_antes = self.getTime()

        if (self.timeout < 0):
            if (self.estado == self.ADELANTE):
                self.estado = self.GIRAR_D
            else:
                self.estado = self.ADELANTE
            self.timeout = TIMEOUT

        if (self.estado == self.ADELANTE):
            self.motores.avanzar_u(self.VEL)
        else:
            self.motores.girar_horario()
        self.motores.hacerPaneoCamara()

    def reset(self):
        pass

    def post_stop(self):
        print('CompWander::post_stop')
        self.timeout = TIMEOUT
        self.estado = self.ADELANTE

    def getTime(self):
        return time.time()
