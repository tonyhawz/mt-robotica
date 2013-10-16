import comp
import time
import config


class CompDescargarLatas(comp.Comp):

    def __init__(self, data, motores,motoresPinza):
        comp.Comp.__init__(self, data)
        self.motores = motores
        self.motoresPinza = motoresPinza
        self.data = data
        self.data.write('DescargandoLatas::','FALSE')

    def takeControl(self):
        return self.data.read('Tacho::disponible') == 1

    def action(self):
        print 'CompDescargarLatas::action'
        self.data.write('DescargandoLatas::','TRUE')
        self.motoresPinza.abrirDescargar()
        time.sleep(config.tiempo_pinza_descarga)
        self.motores.descargarTolva()
        time.sleep(config.tiempo_descarga)
        self.motoresPinza.cerrarDescargar()
        time.sleep(config.tiempo_pinza_descarga)
        self.motores.girar_antihorario()
        time.sleep(config.tiempo_salida_tacho)
        self.data.write('lata::cant_latas', str(0))
        self.data.write('DescargandoLatas::','FALSE')