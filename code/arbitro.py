import time
import threading
import config


class Arbitro(threading.Thread):

    refresh_rate = config.refresh_rate
    current_comp = None
    comps = None
    data = None
    stopped = False

    def __init__(self, comps, data):
        threading.Thread.__init__(self)
        self.comps = comps
        self.current_comp = comps[len(comps)-1]
        i = 0
        for c in self.comps:
            i = i+1
            c.id = i
##      arrancan todos los comportamientos pero quedan pausados
        for c in self.comps :
            c.start()
        time.sleep(3)
        self.data = data
        self.refresh_rate = config.refresh_rate
        self.current_comp.resume()

    def arbitrar(self) :
        self.stopped = False
        while not self.stopped :
            #print 'Arbitro::arbitrando'
            ti =  time.time()
            for c in self.comps :
                if c.takeControl() :
                    if self.current_comp.id != c.id:
                        taux = time.time()
                        print 'Arbitro::arbitrando cambio a ' + str(self.current_comp.id) + ' '  + c.getNombre() + ' ' + str(taux)
                        if self.current_comp != None:
                            self.current_comp.pause()
                        self.current_comp = c
                        self.current_comp.printTiempo(taux)
                        self.current_comp.resume()
                    break;
            tf = time.time()
            delta_t = tf - ti
            # print 'Arbitro::arbitrando ' + str(delta_t)
            time.sleep(self.refresh_rate)

    def run(self):
        self.arbitrar()

    def stop(self):
        self.stopped = True
        for c in self.comps:
            c.stop()


    def get_comps(self):
        return self.comps

    def getNombre(self):
       return 'Arbitro'
