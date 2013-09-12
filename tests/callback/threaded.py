# -*- coding: utf-8 -*-

import threading


class Manager(object):

    def new_thread(self):
        return MyThread(parent=self)

    def on_thread_finished(self, thread, data):
        print 'Manager ' + threading.current_thread().name
        print thread, data


class MyThread(threading.Thread):

    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.parent = parent

    def on_thread_finished(self, thread, data):
        pass

    def run(self):
        # ...
        print 'MyThread ' + threading.current_thread().name
        self.parent and self.parent.on_thread_finished(self, 42)

mgr = Manager()
thread = mgr.new_thread()
print 'Main ' + threading.current_thread().name
thread.start()