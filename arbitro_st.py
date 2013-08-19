import time 
import threading
import config 

class ArbitroST( threading.Thread ) :

    refresh_rate = config.refresh_rate
    comps = None
    data = None
    stopped = False
    
    def __init__(self,comps,data):
        threading.Thread.__init__(self) 
        self.comps = comps
        i = 0 
        for c in self.comps:
            i = i+1 
            c.id = i
        time.sleep(3)
        self.data = data
        self.refresh_rate = config.refresh_rate

    def arbitrar(self) :
        self.stopped = False
        while not self.stopped :
            #print 'Arbitro::arbitrando'
            ti =  time.time()
            for c in self.comps :
                if c.takeControl() :
                    c.action() 
                    break;
            tf = time.time()
            delta_t = tf - ti
            print 'Arbitro::arbitrando ' + str(delta_t)
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

