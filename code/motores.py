#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import time
import config

#DELANTE     = 1
#ATRAS       = 0
#VEL_GIRO    = 680

#global lock_u4b


class Motores():

    def __init__(self, u4b, lock):
        self.butia = u4b
        self.lock = lock

    def refresh(self):
        self.butia.refresh()

    def retroceder_u(self, velocidad):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.atras,
            velocidad,
            config.atras,
            velocidad)
        self.lock.release()

    def avanzar_u(self, velocidad):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.delante,
            velocidad,
            config.delante,
            velocidad)
        self.lock.release()

    def detener(self):
#        self.lock.acquire()
        self.butia.set2MotorSpeed(0, 0, 0, 0, 0)
#        self.lock.release()

    def girar_horario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.delante,
            config.vgiro,
            config.atras,
            config.vgiro)
        self.lock.release()

    def girar_antihorario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.atras,
            config.vgiro,
            config.delante,
            config.vgiro)
        self.lock.release()

    def stop(self):
        self.lock.acquire()
        self.detener()
        self.lock.release()

    def getNombre(self):
        return 'motores'

    def girar_marchatras(self, horario):
        ki = 3
        kd = 3
        if horario:
            ki = 1.8
        else:
            kd = 1.8
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.atras,
            int(round(config.vgiro * ki)),
            config.atras,
            int(round(config.vgiro * kd)), 0)
        self.lock.release()

    #Obtiene la pocion en (x,y) de la camara
    def get_posicion_camara(self):
        x = self.butia.getPosicion(config.id_motor_camara_X)
        y = self.butia.getPosicion(config.id_motor_camara_Y)
        return (x, y)

    def hacerPaneoCamara(self):
        #deberia de ir pasando del centro a la izquierda y luego de la izquierda a la derecha con velocidad constante
        self.butia.setSpeed(config.id_motor_camara_x, config.vel_paneo)
        if self.butia.getPosition(config.id_motor_camara_x) == config.cero_posx_camara:
            #camara centrada => la giro a la izquierda
            self.butia.setPosition(config.id_motor_camara_x,config.max_camara_x)
        elif(self.butia.getPosition(config.id_motor_camara_x)>config.cero_posx_camara):
            #camara iquierda => la giro a la derecha
            self.butia.setPosition(config.id_motor_camara_x,config.max_camara_x)
        elif(self.butia.getPosition(config.id_motor_camara_x)<config.cero_posx_camara):
            #camara  derecha => la giro a la  iquierda
            self.butia.setPosition(config.id_motor_camara_x,config.min_camara_x)

    def centrarCamara(self):
        self.butia.setPosition(config.id_motor_camara_x,
            config.cero_posx_camara)
        self.butia.setPosition(config.id_motor_camara_y,
            config.cero_posy_camara)
