import serial
import os
import time
import matplotlib
import matplotlib.pyplot as plt
import socket
import threading
from bottle import route, run
from bottle import get, post, request, response, redirect
from bottle import static_file
import matplotlib.pyplot as plt

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 1))
ip = s.getsockname()[0]
s.close()
rc = '\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
s = serial.Serial('/dev/ttyS0', baudrate = 9600, timeout = 1)
data = []

def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

def readSensor():
    resp_len = 9
    resp = s.read(resp_len)
    if resp:
        payload = [ord(x) for x in resp[1:-1]]
        crc16 =((sum(payload) % 256) ^ 0xFF) + 1
        return payload

@threaded
def readLoop():
    while 1:
        s.write(rc)
        payload = readSensor()
        concentration = payload[1] * 256 + payload[2]
        data.append(concentration)
        time.sleep(5)

@route('/co2')
def co2():
    plt.plot(data)
    plt.ylabel('co2, ppm')
    plt.grid(True)
    plt.savefig('conc.png', fmt='png')
    return static_file('conc.png', os.getcwd())

readLoop()
run(host=ip, port=80, debug=False)
