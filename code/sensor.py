import threading
import time
import config


class Sensor(threading.Thread):

    stopped = False
    data = None
    refresh_rate = config.refresh_rate
    nombre = None

    def __init__(self,data):
        threading.Thread.__init__(self)
        self.data = data
        self.nombre = 'sensor'

    def run(self) :
        self.stopped = False
        while not self.stopped :
            #print 'Sensor::sensando'
            t0 = time.time()
            self.action()
            tf = time.time()
            #print self.getNombre() + " - " + str(tf-t0)
            time.sleep(self.refresh_rate)
#        print 'Sesnor fuera while'

    def action(self):
        pass

    def stop( self ) :
        self.stopped = True

    def getNombre( self ) :
        return self.nombre
