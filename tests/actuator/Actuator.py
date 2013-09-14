#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Andrés Aguirre Dorelo
# MINA/INCO/UDELAR
# basic ax12 actuator control
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import time

PING = 0x01
READ_DATA = 0x02
WRITE_DATA = 0x03
REG_WRITE = 0x04
ACTION = 0x05
RESET = 0x06
SYNC_WRITE = 0x83



SIM_HOST = 'localhost'
SIM_PORT = 7777

GOAL_POSITION_CMD = 0X1E
MOVING_SPEED_CMD = 0x20
TURN_LED_CMD = 0x19
CW_ANGLE_CMD = 0x06
CCW_ANGLE_CMD = 0x08
VOLTAGE_CMD = 0x0C
PRESENT_VOLTAGE_CMD = 0x2A
MAX_TORQUE_CMD = 0x0E
TORQUE_LIMIT_CMD = 0x22
TORQUE_ENABLE_CMD = 0x18
PRESENT_POSITION = 0x24

CCW_CMD = 0x08

class Actuator:

    def __init__(self, communication):
        self.communication = communication

    def checksum_check(self, msg):
        checksum = 0
        for i in range(2, len(msg)):
            checksum = (checksum + msg[i]) % 256
        checksum = 255 - checksum
        return checksum

    def make_msg(self, id, instruction, parameters):
        msg = []
        length_field = len(parameters) + 2
        msg = [0xff, 0xff, id, length_field, instruction] + parameters
        checksum = self.checksum_check(msg)
        msg.append(checksum)
        return msg

    def move_actuator(self, idMotor, goal_position, angular_speed):
        goal_position_low = goal_position & 0xff
        goal_position_high = (goal_position & 0xff00) >> 8
        angular_speed_low = angular_speed & 0xff
        angular_speed_high = (angular_speed & 0xff00) >> 8
        msg = self.make_msg(idMotor, WRITE_DATA, [GOAL_POSITION_CMD, goal_position_low, goal_position_high, angular_speed_low, angular_speed_high])
        self.communication.send_msg(msg)

    def set_speed_actuator(self, id, angular_speed, CW_bit):
        '''

        '''
        angular_speed_low = angular_speed & 0xff
        angular_speed_high = (angular_speed & 0xff00) >> 8
        angular_speed_high = angular_speed_high + 0x04 * CW_bit
        msg = self.make_msg(id, WRITE_DATA, [MOVING_SPEED_CMD, angular_speed_low, angular_speed_high])
        self.communication.send_msg(msg)

    #Setear la posición angular máxima en la que opera el motor. Si la máxima (CCW)
    #y la mínima (CW) son ambas 0 se entra en modo de giro continuo.
    #0x3ff equivale a 300º, entre 300º y 360º es ángulo ciego, sólo se pasa por él en
    #caso de giro continuo.
    #ccw_position de 16 bits
    def set_ccw(self, id, ccw_position):
        ccw_position_low = ccw_position & 0xff
        ccw_position_high = (ccw_position & 0xff00) >> 8
        msg = self.make_msg(id, WRITE_DATA, [CCW_CMD,ccw_position_low, ccw_position_high])
        self.communication.send_msg(msg)



    def set_speed_actuator_RW(self, id, angular_speed, CW_bit):
        angular_speed_low = angular_speed & 0xff
        angular_speed_high = (angular_speed & 0xff00) >> 8
        angular_speed_high = angular_speed_high + 0x04 * CW_bit
        msg = self.make_msg(id, REG_WRITE, [MOVING_SPEED_CMD, angular_speed_low, angular_speed_high])
        self.communication.send_msg(msg)


    def led_state_change(self, id, led_state):
        msg = self.make_msg(id, WRITE_DATA, [TURN_LED_CMD, led_state])
        self.communication.send_msg(msg)

    def setear_id(self, idaponer):
        msg = self.make_msg(0xFE, WRITE_DATA, [0x03, idaponer])
        self.communication.send_msg(msg)

    def set_AngleLimit(self, id, CW_angle, CCW_angle):
        '''
        esto sirve para ponerlo en modo de giro libre
        '''
        CW_angle_low = CW_angle & 0xff
        CW_angle_high = (CW_angle & 0xff00) >> 8
        CCW_angle_low = CCW_angle & 0xff
        CCW_angle_high = (CCW_angle & 0xff00) >> 8
        msg = self.make_msg(id, WRITE_DATA, [CW_ANGLE_CMD, CW_angle_low, CW_angle_high, CCW_angle_low, CCW_angle_high])
        self.communication.send_msg(msg)

    def set_voltage(self, idMotor, V_min, V_max):
        '''
        COnfigura el registro VOLTAGE y VOLTAGE + 1 a los valores V_min x 10 y V_max x 10
        respectivamente en el motor de id = idMotor
        '''
        msg = self.make_msg(idMotor, WRITE_DATA, [VOLTAGE_CMD, (V_min * 10), (V_max * 10)])
        self.communication.send_msg(msg)

    def consultar_velocidad(self, idMotor):
        self.communication.flushInput()  # vacia el buffer de datos de entrada
        msg = self.make_msg(idMotor, READ_DATA, [MOVING_SPEED_CMD, 0x02])  # parametros =[dir de memoria inicial, bytes a leer]
        self.communication.send_msg(msg)  # efectua el pedido de lectura de la ID
        aux = self.communication.read_msg(0x02)  # cuantos parametros espero, devuelve array
        # faltaria procesar los dos bprtes en una velocidad unica con un sentido de giro
        print "probando"
        # aux2 = (hex(ord(aux[1])))
        alto = ord(aux[1]) & 0x3
        dir = ord(aux[1]) & 0x4
        if (dir != 0):
            dir = 1
        else :
            dir = -1
        print alto
        alto = alto << 8
        total = alto + ord(aux[0])
        print total
        print "/probando"
        return dir * total
        # return ord(aux[0])

    def consultar_voltaje(self, idMotor):
        self.communication.flushInput()  # vacia el buffer de datos de entrada
        msg = self.make_msg(idMotor, READ_DATA, [PRESENT_VOLTAGE_CMD, 0x01])  # parametros =[dir de memoria inicial, bytes a leer]
        self.communication.send_msg(msg)  # efectua el pedido de lectura de la ID
        aux = self.communication.read_msg(1)  # cuantos parametros espero, devuelve array
        # faltaria procesar el byte recibido en una saliad de voltaje en Volts
        final = (float)(ord(aux[0])) / 10
        return final

    def consultar_torqueMaximo(self, idMotor):
        self.communication.flushInput()  # vacia el buffer de datos de entrada
        # msg = self.make_msg(idMotor, READ_DATA, [MAX_TORQUE_CMD, 0x02]) # parametros =[dir de memoria inicial, bytes a leer]
        msg = self.make_msg(idMotor, READ_DATA, [TORQUE_LIMIT_CMD, 0x02])
        self.communication.send_msg(msg)  # efectua el pedido de lectura de la ID
        aux = self.communication.read_msg(2)  # cuantos parametros espero, devuelve array
        # faltaria procesar el byte recibido en una saliad de voltaje en Volts
        print "probando"
        # aux2 = (hex(ord(aux[1])))
        alto = ord(aux[1]) & 0x3
        print alto
        alto = alto << 8
        total = alto + ord(aux[0])
        print total
        print "/probando"
        return total

    def setTorqueMaximo(self, idMotor, maxTorque):
        if (maxTorque > 1023):
            msg = self.make_msg(idMotor, WRITE_DATA, [MAX_TORQUE_CMD, 0xFF, 0x3])
            msg2 = self.make_msg(idMotor, WRITE_DATA, [TORQUE_LIMIT_CMD, 0xFF, 0x3])
        else:
            torque_low = maxTorque & 0xff
            torque_high = (maxTorque & 0xff00) >> 8
            msg = self.make_msg(idMotor, WRITE_DATA, [MAX_TORQUE_CMD, torque_low, torque_high])
            msg2 = self.make_msg(idMotor, WRITE_DATA, [TORQUE_LIMIT_CMD, torque_low, torque_high])
        self.communication.send_msg(msg)
        self.communication.send_msg(msg2)

    def test (self, idMotor):
        self.communication.flushInput()
        msg = self.make_msg(idMotor, WRITE_DATA, [0x10, 0x01])
        self.communication.send_msg(msg)

    def reset (self, idMotor):
        msg = self.make_msg(idMotor, RESET, [])
        self.communication.send_msg(msg)

    def setTorque(self, idMotor, enable):
        if (enable):
            torque = 0x1
        else :
            torque = 0x0
        msg = self.make_msg(idMotor, WRITE_DATA, [TORQUE_ENABLE_CMD, torque])
        self.communication.send_msg(msg)

    # def action(self,idMotor):

    def action(self):
        msg = self.make_msg(0xFE , ACTION, [])
        self.communication.send_msg(msg)

    def mover_2_motoresA(self, idI, idD, Vel, CW_bit, radio, distancia, k):
        '''
        Funcion Para mover 2 motores hacia adelante o atras con misma velocidad
        Parametros:
          idI:    id motor izquierda
          idD:    id motor Derecha
          Vel:    velocidad Angular
          CW_bit: sentido de giro (0 antihorario, 1 horario)
          dist:   distancia en metros que me quiero mover.
          radio:  radio Rueda
          k:      constante de ajuste empirica
        '''
        if (k <= 0):
            k = 1
        # Seteo los margenes antihorario y horario en cero para estar en rueda libre.
        self.set_AngleLimit(idI, 0x0000, 0x0000)
        self.set_AngleLimit(idI, 0x0000, 0x0000)

        diametroRueda = 2 * 3.1416 * radio
        print diametroRueda

        # Paso mi velocidad a RPS
        Vel2 = ((float(Vel) * 114.0) / 0x3ff) / 60.0
        # calculo cantidad de tiempo que me tengo que mover a la velocidad dada para llegar a la distancia pedida.
        t = distancia / (k * Vel2 * diametroRueda)
        # Seteo las velocidades de cada Motor con REG_WRITE

        aux_bit = 1
        if (CW_bit == 1):
            aux_bit = 0

        self.set_speed_actuator_RW(idI, Vel, CW_bit)
        self.set_speed_actuator_RW(idD, Vel, aux_bit)
        # Activo los mensajes (se van a mover ya que estan en modo rueda libre y les di una velocidad)
        self.action()
        # Seteo las velocidades a cero de cada Motor con REG_WRITE para activarlo cuando se termine el tiempo aun
        self.set_speed_actuator_RW(idI, 0, CW_bit)
        self.set_speed_actuator_RW(idD, 0, CW_bit)
        # espero el tiempo especificado
        time.sleep(t)
        # Pongo en cero la velocidad
        self.action()


    def girar(self, angulo, idI, idD, Vel, der, radio, radioCM, k):  # angulo que se quiere girar, ids de los motores, velocidad, derecha
        '''
        # Funcion Para girar determinado angulo con Sentido
        #
        #    Parametros: idI: id motor izquierda
        #                idD: id motor Derecha
        #                angulo: angulo a girar
        #                Vel: velocidad Angular
        #                der: vale uno si giro hacia derecha 0 caso izquierda
        #                radio:radio Rueda
        #                radioCM: distancia de la rueda respecto al centro de masa (asumo ambas ruedas equidistantes)
        #                k: constante de ajuste empirica
        # Asumimos rodadura sin deslizar( punto de contacto con el suelo tiene v=0, f_roz estatico), y probaremos valores para estar en dicha condicion.
        '''
        # Seteo los margenes antihorario y horario en cero para estar en rueda libre.
        self.set_AngleLimit(idI, 0x0000, 0x0000)
        self.set_AngleLimit(idD, 0x0000, 0x0000)

        if (der == 1):
            print "der = 1"
            self.set_speed_actuator_RW(idI, Vel, 0)
            self.set_speed_actuator_RW(idD, Vel, 0)
        else:
            print "der = 0"
            self.set_speed_actuator_RW(idI, Vel, 1)
            self.set_speed_actuator_RW(idD, Vel, 1)
        # Paso mi velocidad a RPS
        Vel2 = ((float(Vel) * 114.0) / 0x3ff) / 60.0
        # Segmento de Cfa que se debe recorrer girando el angulo deseado teniendo el centro de masa fijo
        cfa = (angulo * 3.1416 / 180.0) * radioCM  # Spase el angulo a radianes
        # tiempo que debe estar la rueda funcionando para recorrer esa cfa
        t = cfa / (k * (Vel2 * 2 * 3.1416 * radio))  # Falta fijarse en q unidad estaria la Vel.
        # cargo valores
        self.action()
        # configuro la velocidad en 0 para cargarse al finalizar el tiempo
        self.set_speed_actuator_RW(idI, 0, 0)
        self.set_speed_actuator_RW(idD, 0, 0)
        # espero el tiempo
        time.sleep(t)
        self.action()

    def consultar_posicion(self, idMotor):
        '''
        Consulta la posicion del motor en un momento dado.
        '''
        self.communication.flushInput()  # vacia el buffer de datos de entrada
        msg = self.make_msg(idMotor, READ_DATA, [PRESENT_POSITION, 0x02])  # parametros =[dir de memoria inicial, bytes a leer]
        self.communication.send_msg(msg)  # efectua el pedido de lectura de la ID
        aux = self.communication.read_msg(2)  # cuantos parametros espero, devuelve array
        bit_Alto=ord(aux[0])
        bit_Bajo=ord(aux[1])
        bit_Alto= bit_Alto << 8
        final = bit_Bajo + bit_Alto
        return final


