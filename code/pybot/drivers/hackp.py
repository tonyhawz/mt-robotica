
RD_VERSION = 0x00
SET_MODE = 0x01
READ = 0x02
WRITE = 0x03
WRITE_PORT = 0x04
PORT_IN = 0x05
PORT_OUT = 0x06


f1 = {
    'name': 'getVersion',
    'call': RD_VERSION,
    'params': 0,
    'read': 3
}

f2 = {
    'name': 'setMode',
    'call': SET_MODE,
    'params': 2,
    'read': 1
}

f3 = {
    'name': 'read',
    'call': READ,
    'params': 1,
    'read': 1
}

f4 = {
    'name': 'write',
    'call': WRITE,
    'params': 2,
    'read': 1
}

FUNCTIONS = [f1, f2, f3, f4]

