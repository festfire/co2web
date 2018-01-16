import serial
import os
import sched
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
path = '/dev/shm'
rc = '\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
s = serial.Serial('/dev/ttyS0', baudrate = 9600, timeout = 1)
data = list(xrange(360))
timer = sched.scheduler(time.time, time.sleep)
def readSensor():
    resp_len = 9
    resp = s.read(resp_len)
    if resp:
        payload = [ord(x) for x in resp[1:-1]]
        crc16 =((sum(payload) % 256) ^ 0xFF) + 1
        return payload

def readLoop(sc):
    timer.enter(10, 1, readLoop, (sc,))
    s.write(rc)
    payload = readSensor()
    concentration = payload[1] * 256 + payload[2]
    temp = payload[3]-40
    data.append(concentration)
    data.pop(0)
    plt.plot(data)
    plt.ylabel('co2, ppm')
    plt.xticks([0, 90, 180, 270, 360], ('-60', '-45', '-30', '-15', '0') )
    plt.xlabel('time, m')
    plt.grid(True)
    plt.title('temp: ' + str(temp) + 'C, last: ' + str(concentration) + 'ppm')
    plt.savefig(path +'/conc.png', fmt='png')
    plt.clf()

timer.enter(10, 1, readLoop, (timer,))
timer.run()
