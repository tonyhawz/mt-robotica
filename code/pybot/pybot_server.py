#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Pybot server
#
# Copyright (c) 2012-2013 Butiá Team butia@fing.edu.uy 
# Butia is a free and open robotic platform
# www.fing.edu.uy/inco/proyectos/butia
# Facultad de Ingeniería - Universidad de la República - Uruguay
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

import sys
import select
import socket
import usb4butia

argv = sys.argv[:]

PYBOT_HOST = 'localhost'
PYBOT_PORT = 2009
BUFSIZ = 1024
MAX_CLIENTS = 4


class Server():

    def __init__(self, debug=False):
        self.debug = debug
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((PYBOT_HOST, PYBOT_PORT))
        self.socket.listen(MAX_CLIENTS)
        self.clients = {}
        self.robot = usb4butia.USB4Butia(self.debug)

    def call_aux(self, modulename, board_number, number, function, params):
        if modulename == 'lback':
            par = params
        else:
            par = []
            for e in params:
                par.append(int(e))
        return self.robot.callModule(modulename, board_number, number, function, par)

    def init_server(self):

        inputs = [self.socket]

        run = True
        while run:

            try:
                inputready,outputready,exceptready = select.select(inputs, [], [])
            except Exception, err:
                print 'Error in select', err
                break

            for s in inputready:
                if s == self.socket:
                    client, addr = self.socket.accept()
                    print 'New client: ', str(addr)
                    inputs.append(client)
                    self.clients[client] = addr
                else:
                    data = s.recv(BUFSIZ)
                    if data:
                        result = ''
                        # remove end line characters if become from telnet
                        r = data.replace('\r', '')
                        r = r.replace('\n', '')
                        r = r.split(' ')

                        #print 'split', r

                        if len(r) > 0:
                            if r[0] == 'QUIT':
                                result = 'BYE'
                                run = False
                            elif r[0] == 'CLIENTS':
                                first = True
                                for c in self.clients:
                                    addr = self.clients[c]
                                    if first:
                                        result = result + str(addr[0]) + ', ' + str(addr[1]) 
                                        first = False
                                    else:
                                        result = result + '\n' + str(addr[0]) + ', ' + str(addr[1]) 
                            elif r[0] == 'LIST':
                                l = self.robot.get_modules_list()
                                result = ','.join(l)
                            elif r[0] == 'REFRESH':
                                self.robot.refresh()
                            elif r[0] == 'BUTIA_COUNT':
                                result = self.robot.get_butia_count()
                            elif r[0] == 'CALL':
                                if len(r) >= 3:
                                    board = 0
                                    number = 0
                                    mbn = r[1]
                                    if mbn.count('@') > 0:
                                        modulename, bn = mbn.split('@')
                                        board, number = bn.split(':')
                                    else:
                                        if mbn.count(':') > 0:
                                            modulename, number = mbn.split(':')
                                        else:
                                            modulename = mbn
                                    function = r[2]
                                    par = r[3:]
                                    result = self.call_aux(modulename, int(board), int(number), function, par)

                        result = str(result)
                        try:
                            s.send(result + '\n')
                        except:
                            print 'Send fails'

                    else:
                        s.close()
                        inputs.remove(s)
                        self.clients.pop(s)
                        
        print 'Closing server'
        self.socket.close()
        self.robot.close()


if __name__ == "__main__":
    if 'DEBUG' in argv:
        s = Server(True)
    else:
        s = Server()
    s.init_server()

