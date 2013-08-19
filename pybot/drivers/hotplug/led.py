
RD_VERSION = 0x00
TURN = 0x01

f1 = {
    'name': 'getVersion',
    'call': RD_VERSION,
    'params': 0,
    'read': 3
}

f2 = {
    'name': 'turn',
    'call': TURN,
    'params': 1,
    'read': 1
}

FUNCTIONS = [f1, f2]
