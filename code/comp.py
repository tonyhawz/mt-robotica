import threading
import time
import config


class Comp(threading.Thread):

    refresh_rate = config.refresh_rate
    stopped = False
    paused = True
    data = None
    id = 0

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
        self.state = threading.Condition()

    def run(self):
#        self.stopped = False
#       Solo stopped == True cuando realmente se va a parar de ejecutar
        while not self.stopped:

            with self.state:
#               Si paused me duermo
                if self.paused:
                    self.state.wait()

            if not self.stopped:
                self.action()
            time.sleep(self.refresh_rate)

#        threading.Thread.__init__(self)
        self.post_stop()

    def takeControl(self):
        return True

    def printTiempo(self, tiempo):
        print str(time.time() - tiempo)

#   Despierta el hilo para que siga ejecutando
    def resume(self):
        self.reset()
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True

    def stop(self):
        self.stopped = True
        self.resume()

    def post_stop(self):
        pass

    def action(self):
        print 'comp::action ' + str(time.time())
        pass

    def reset(self):
        pass

    def getNombre(self):
        return 'Comp(generico)'

