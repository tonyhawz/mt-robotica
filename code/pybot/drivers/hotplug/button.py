
RD_VERSION = 0x00
GET_VALUE = 0x01

f1 = {
    'name': 'getVersion',
    'call': RD_VERSION,
    'params': 0,
    'read': 3
}

f2 = {
    'name': 'getValue',
    'call': GET_VALUE,
    'params': 0,
    'read': 2
}

FUNCTIONS = [f1, f2]
