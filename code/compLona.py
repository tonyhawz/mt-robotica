import comp
import time
import config


class CompLona(comp.Comp):

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
        return 'CompLona'

    def leerSensores(self):
        v1 = True
        v2 = True
        try:
            v1 = self.data.read('Camara::barra_der') is 'OK'
        except KeyError:
            v1 = True
        try:
            v2 = self.data.read('Camara::barra_izq') is 'OK'
        except KeyError:
            v2 = True
        return [v1, v2]

    def takeControl(self):
        try:
            cargando = self.data.read('CargandoLata::')
            if cargando is 'TRUE':
                return False
        except KeyError:
            pass
        if self.estado == config.cero:
            v1, v2 = self.leerSensores()
            self.t_antes = self.getTime()
            if not v1:
                self.horario = True
                self.estado = config.uno
                self.timeout = self.timeout_ini
                return True
            elif not v2:
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
        print (('CompLona::action estado:' + self.getNombreEstado() + ' '
        + str(self.timeout) + ' time:' + str(time.time())))
        self.t_antes = self.getTime()

        if (self.timeout < 0):
            self.estado = (self.estado + 1) % 2

        if (self.estado == config.uno):
            #self.motores.girar_marchatras(self.horario)
            if self.horario:
                self.motores.girar_horario()
            else:
                self.motores.girar_antihorario()

    def reset(self):
        self.timeout = self.timeout_ini
        self.estado = config.cero
        self.t_antes = self.getTime()

    def post_stop(self):
        pass

    def getTime(self):
        return time.time()

    def getNombreEstado(self):
        if self.estado is 0:
            return 'OK'
        elif self.estado is 1 and self.horario:
            return 'GIRAR HORARIO'
        elif self.estado is 1 and not self.horario:
            return 'GIRAR ANTIHORARIO'