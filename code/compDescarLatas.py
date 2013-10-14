import comp
import time
import config


class CompDescargarLatas(comp.Comp):

    def __init__(self, data, motores):
        comp.Comp.__init__(self, data)
        self.motores = motores

    def takeControl(self):
        return self.data.read('Tacho::disponible') == 1

    def action(self):
        print 'CompDescargarLatas::action'
        self.motores.descargarTolva()
        self.motores.girar_antihorario()
        time.sleep(config.tiempo_salida_tacho)