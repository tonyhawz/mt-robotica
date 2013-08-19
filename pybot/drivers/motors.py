
RD_VERSION = 0x00
SET_VEL_2MTR = 0x01
SET_VEL_MTR = 0x02

f1 = {
    'name': 'getVersion',
    'call': RD_VERSION,
    'params': 0,
    'read': 3
}

f2 = {
    'name': 'setvel2mtr',
    'call': SET_VEL_2MTR,
    'params': 6,
    'read': 1
}

f3 = {
    'name': 'setvelmtr',
    'call': SET_VEL_MTR,
    'params': 4,
    'read': 1
}

FUNCTIONS = [f1, f2, f3]
