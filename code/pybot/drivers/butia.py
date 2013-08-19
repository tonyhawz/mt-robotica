
RD_VERSION = 0x02
GET_VOLT = 0x03

f1 = {
    'name': 'read_ver',
    'call': RD_VERSION,
    'params': 0,
    'read': 2
}

f2 = {
    'name': 'get_volt',
    'call': GET_VOLT,
    'params': 0,
    'read': 2
}

FUNCTIONS = [f1, f2]
