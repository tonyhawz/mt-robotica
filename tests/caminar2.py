# -*- coding: utf-8 -*-
import sys
import time
#import threading

sys.path.append("../code/")

from myUsb4Butia import MyUsb4Butia
#from motores import Motores
#from myUsb4Butia import MyUsb4Butia


class Caminar():

    def __init__(self):
        #super(Caminar, self).__init__()
        self.b = MyUsb4Butia()

    def adelante(self):
        self.b.set2MotorSpeed(1, 1000, 1, 1000)
        time.sleep(2)
        self.b.set2MotorSpeed(1, 0, 1, 0)


def main(argv):
    c = Caminar()
    c.adelante()


if __name__ == "__main__":
    main(sys.argv[:])
