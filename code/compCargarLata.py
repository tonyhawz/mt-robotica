import comp
import time
import config
import threading


class CompCargarLata(comp.Comp):

    estado = 0 # nada

    def __init__(self, data, pinzas, motores):
        comp.Comp.__init__(self, data)
        self.data.write('Camara::lata_y', 0)
        self.data.write('Camara::lata_x', 0)
        self.pinzas = pinzas
        self.data.write('lata::cant_latas', '0')
        self.pinzas.abierta()
        self.motores = motores

    def takeControl(self):
        x = self.data.read('Camara::lata_x')
        y = self.data.read('Camara::lata_y')
        encontro = self.data.read('Camara::encontro') is 'TRUE'
        #print str(x) + '::' + str(y) + '::::minx ' + str(config.min_x) + '::' + 'maxx' + str(config.max_x)  + ' :: miny' +  str(config.min_y)
        ret = x > config.min_x and x < config.max_x and y > config.min_y and encontro
        return ret

    def action(self):
        if self.estado is 0:
            self.estado = 1
            #cargand
            print 'CompCargarLata::action'
            self.motores.detener()
            self.data.write('CargandoLata::', 'TRUE')
            self.pinzas.aCargar()
            time.sleep(3)
            self.pinzas.cargar()
            time.sleep(2)
            self.pinzas.abierta()
            time.sleep(3)
            self.estado = 0
            self.data.write('CargandoLata::', 'FALSE')
            latas = int(self.data.read('lata::cant_latas')) + 1
            self.data.write('lata::cant_latas', str(latas))
            #a = actitud(self.data,self.pinzas)

    def reset(self):
        pass

    def post_stop(self):
        print 'CompCargarLata::post_stop'


class actitud(threading.Thread):

    def __init__(self, data, pinzas):
        threading.Thread.__init__(self)
        self.data = data
        self.pinzas = pinzas

