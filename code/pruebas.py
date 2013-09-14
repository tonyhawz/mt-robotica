from myUsb4Butia import MyUsb4Butia

WRITE_INFO = 0x01

def checksum_check( msg):
    checksum = 0
    for i in range(2, len(msg)):
        checksum = (checksum + msg[i]) % 256
    checksum = 255 - checksum
    return checksum

def make_msg( id, instruction, parameters):
    msg = []
    length_field = len(parameters) + 2
    msg = [0xff, 0xff, id, length_field, instruction] + parameters
    checksum = checksum_check(msg)
    msg.append(checksum)
    return msg

coso = MyUsb4Butia()

speed = 1000
inverse = 1
#inverse ^=1
speed |= inverse*1024
msg = make_msg(WRITE_INFO,0x20,[speed/256,speed%256])
print (msg)
ret = coso.sendPacket(1,msg)
print(ret)
print(coso.getVersionAx())
print(coso.setSpeed(1,1500))