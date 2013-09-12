import comp
import time
import config


class CompAlfombra(comp.Comp):

    indice_izq = config.grisIzq
    indice_der = config.grisDer

    timeout_ini = config.timeout_ini
    timeout = None
    t_antes = None
    estado = None

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.timeout = self.timeout_ini
        self.motores = motores
        self.estado = config.cero
        self.t_antes = self.getTime()

    def getNombre(self):
        return 'CompAlfombra'

    def leerSensores(self):
        v1 = 0
        v2 = 0
        try:
            v1 = self.data.read('SensorGrises::' + str(self.indice_izq))
        except KeyError:
            vi = 0
        try:
            v2 = self.data.read('SensorGrises::' + str(self.indice_der))
        except KeyError:
            v2 = 0
        return [v1, v2]

    def takeControl(self):
        if self.estado == config.cero:
            v1, v2 = self.leerSensores()
            self.t_antes = self.getTime()
            if v1 > config.alf_detect:
                self.horario = True
                self.estado = config.uno
                self.timeout = self.timeout_ini
                return True
            elif v2 > config.alf_detect:
                self.horario = False
                self.estado = config.uno
                self.timeout = self.timeout_ini
                return True
            else:
                return False
        else:
            v1, v2 = self.leerSensores()
            if (v1 > config.alf_detect or v2 > config.alf_detect):
                self.timeout = self.timeout_ini
            return True

    def action(self):
        deltaT = self.getTime() - self.t_antes
        self.timeout = self.timeout - deltaT
        print (('CompAlfombra::action estado:' + str(self.estado) + ' '
        + str(self.timeout) + ' time:' + str(time.time())))
        self.t_antes = self.getTime()

        if (self.timeout < 0):
            self.estado = (self.estado + 1) % 2

        if (self.estado == config.uno):
            self.motores.girar_marchatras(self.horario)

    def reset(self):
        self.timeout = self.timeout_ini
        self.estado = config.cero
        self.t_antes = self.getTime()

    def post_stop(self):
        pass

    def getTime(self):
        return time.time()
