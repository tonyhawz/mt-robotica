# -*- coding: utf-8 -*-
import sys
import time
import threading

sys.path.append("../code/")

from myUsb4Butia import MyUsb4Butia
from motores import Motores


class Caminar():

    def __init__(self):
        #super(Caminar, self).__init__()
        self.b = MyUsb4Butia()
        self.l = threading.Lock()
        self.m = Motores(self.b, self.l)

    def adelante(self):
        self.m.avanzar_u(1000)
        time.sleep(2)
        self.m.detener()


def main(argv):
    c = Caminar()
    c.adelante()


if __name__ == "__main__":
    main(sys.argv[:])
