import comp
import time
import config

CERO = 0
UNO = 1


class CompEvitar(comp.Comp):

    timeout_ini = 4
    timeout = None
    t_antes = None
    estado = None

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.timeout = self.timeout_ini
        self.motores = motores
        self.estado = config.cero
        self.t_antes = self.getTime()
        self.data.write('CargandoLata::', 'FALSE')
        self.data.write('DescargandoLatas::', 'FALSE')

    def takeControl(self):
        try:
            cargando = self.data.read('CargandoLata::')
            if cargando is 'TRUE':
                return False
            cargando = self.data.read('DescargandoLatas::')
            if cargando is 'TRUE':
                return False
        except KeyError:
            pass
        if self.estado is config.cero:
            dist = 0
            try:
                dist = self.data.read( 'SensorDistancia::' + str(config.idDistIzq))
            except KeyError:
                dist = 0
            cargando = self.data.read('CargandoLata::')
            self.t_antes = self.getTime()
            if dist > config.dist_min and cargando is not '1':
                self.horario = False
                self.estado = config.uno
                self.timeout = self.timeout_ini
                return True
            else:
                dist = 0
                try:
                    dist = self.data.read('SensorDistancia::' + str(config.idDistDer))
                except KeyError:
                    dist = 0
                cargando = self.data.read('CargandoLata::')
                self.t_antes = self.getTime()
                if dist > config.dist_min and cargando is not '1':
                    self.horario = False
                    self.estado = config.uno
                    self.timeout = self.timeout_ini
                    return True
                else:
                    return False
        else:
            return True

    def action(self):
        print 'CompEvitar::action'
        deltaT = self.getTime() - self.t_antes
        self.timeout = self.timeout - deltaT
        self.t_antes = self.getTime()

        if (self.timeout < 0):
            self.estado = (self.estado + 1) % 2
        if (self.estado == config.uno):
            self.motores.girar_horario()#ver que hace para evitar
            #print "ESQUIVAR!!!"

    def reset(self):
        self.timeout = self.timeout_ini
        self.estado = config.cero
        self.t_antes = self.getTime()

    def post_stop(self):
        print('CompEvitar::post_stop')

    def getTime(self):
        return time.time()

    def getNombre(self):
        return 'CompEvitar'