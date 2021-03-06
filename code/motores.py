#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
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

    def avanzar_horario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.delante,
            config.vgiro,
            config.delante,
            config.vgiromenor)
        self.lock.release()

    def avanzar_antihorario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.delante,
            config.vgiromenor,
            config.delante,
            config.vgiro)
        self.lock.release()

    def detener(self):
#        self.lock.acquire()
        self.butia.set2MotorSpeed(0, 0, 0, 0, 0)
#        self.lock.release()

    def girar_horario(self):
        self.lock.acquire()

        self.butia.set2MotorSpeed(config.atras,
            config.vgiro,
            config.atras,
            config.vgiromenor)
        #time.sleep(0.1)
        #self.butia.set2MotorSpeed(config.delante,
            #config.VEL,
            #config.delante,
            #config.VEL)
        #time.sleep(0.1)
        #self.butia.set2MotorSpeed(0,0,0,0)
        self.lock.release()

        #self.butia.set2MotorSpeed(config.delante,
            #config.vgiromenor,
            #config.atras,
            #config.vgiro)


    def girar_antihorario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.atras,
            config.vgiromenor,
            config.atras,
            config.vgiro)
        #time.sleep(0.1)
        #self.butia.set2MotorSpeed(config.delante,
            #config.VEL,
            #config.delante,
            #config.VEL)
        #time.sleep(0.1)
        #self.butia.set2MotorSpeed(0,0,0,0)
        self.lock.release()

    def girar_lugar_antihorario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.atras,
            config.vgirobusqueda,
            config.delante,
            config.vgirobusqueda)
        self.lock.release()

    def girar_lugar_horario(self):
        self.lock.acquire()
        self.butia.set2MotorSpeed(config.delante,
            config.vgirobusqueda,
            config.atras,
            config.vgirobusqueda)
        self.lock.release()

    def stop(self):
        self.lock.acquire()
        self.detener()
        self.lock.release()

    def getNombre(self):
        return 'motores'

    def girar_marchatras(self, horario):
        i = 1
        d = 1
        if horario:
            i = 0
        elif not horario:
            d = 0
        self.lock.acquire()
        self.butia.set2MotorSpeed(i,
            config.vgiro,
            d,
            config.vgiro, 0)
        self.lock.release()

    def girar_marchatras_viejo(self, horario):
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
        x = self.butia.getPosition(config.id_motor_camara_X)
        y = self.butia.getPosition(config.id_motor_camara_Y)
        return (x, y)

    def hacerPaneoCamara(self):
        #deberia de ir pasando del centro a la izquierda y luego de la izquierda a la derecha con velocidad constante
        self.butia.setSpeed(config.id_motor_camara_X, config.vel_paneo)
        if self.butia.getPosition(config.id_motor_camara_X) == config.cero_posx_camara:
            #camara centrada => la giro a la izquierda
            self.butia.setPosition(config.id_motor_camara_X,config.max_camara_x)
        elif(self.butia.getPosition(config.id_motor_camara_X)>config.cero_posx_camara):
            #camara iquierda => la giro a la derecha
            self.butia.setPosition(config.id_motor_camara_X,config.min_camara_x)
        elif(self.butia.getPosition(config.id_motor_camara_X)<config.cero_posx_camara):
            #camara  derecha => la giro a la  iquierda
            self.butia.setPosition(config.id_motor_camara_X,config.max_camara_x)

    def girarCamaraIzquierda(self):
        self.butia.setSpeed(config.id_motor_camara_X, config.vel_paneo)
        self.butia.setPosition(config.id_motor_camara_X,self.butia.getPosition(config.id_motor_camara_X)+config.alfa_giro)

    def girarCamaraDerecha(self):
        self.butia.setSpeed(config.id_motor_camara_X, config.vel_paneo)
        self.butia.setPosition(config.id_motor_camara_X,self.butia.getPosition(config.id_motor_camara_X)-config.alfa_giro)


    def centrarCamara(self):
        self.butia.setPosition(config.id_motor_camara_X,
            config.cero_posx_camara)
        self.butia.setPosition(config.id_motor_camara_Y,
            config.cero_posy_camara)

    def posicion_levantar(self):
        speed = config.motor_pinza_speed
        self.setPosition(config.motor_pinza_d_2, 511, speed)
        self.setPosition(6, 511, speed)
        self.setPosition(5, 200, speed)
        self.setPosition(7, 811, speed)

    def initMotorPinza(self, motor_id, speed):
        self.butia.jointMode(motor_id, 0, 1023)
        self.butia.setSpeed(motor_id, speed)

    def setPositionPinza(self, motor_id, pos, speed=None):
        self.initMotorPinza(motor_id, speed)
        self.butia.setPosition(motor_id, pos)

    def setPositionTolva(self, pos, speed=None):
        self.initMotorPinza(config.id_motor_tolva, speed)
        self.butia.setPosition(config.id_motor_tolva, pos)

    def descargarTolva(self):
        self.setPositionTolva(config.tolva_pos_final,config.tolva_vel)
        time.sleep(2)
        self.setPositionTolva(config.tolva_pos_init,config.tolva_vel)


