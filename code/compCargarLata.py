import comp
import time
import config

class CompCargarLata(comp.Comp):

    def __init__(self, data, pinzas):
        comp.Comp.__init__(self, data)
        self.data.write('Camara::lata_y', 0)
        self.data.write('Camara::lata_x', 0)
        self.pinzas = pinzas

    def takeControl(self):
        x = self.data.read('Camara::lata_x')
        y = self.data.read('Camara::lata_y')
        return x > config.min_x and x < config.max_x and y > config.min_y

    def action(self):
        print 'CompCargarLata::action'

        self.pinzas.
        self.motores.girar_antihorario()
        self.motores.girar_horario()
        self.motores.girar_antihorario()
        self.motores.girar_horario()
        self.motores.girar_antihorario()
        self.motores.girar_horario()
        self.motores.detener()

        latas = self.data.read('lata::cant_latas') + 1
        self.data.write('lata::cant_latas', latas)

    def reset(self):
        pass

    def post_stop(self):
        print 'CompCargarLata::post_stop'

