
RESET = 0xFF
GET_FIRMWARE_VERSION = 0xFE

f1 = {
    'name': 'reset',
    'call': RESET,
    'params': 0,
    'read': 0
}

f2 = {
    'name': 'getVersion',
    'call': GET_FIRMWARE_VERSION,
    'params': 0,
    'read': 1
}

FUNCTIONS = [f1, f2]
