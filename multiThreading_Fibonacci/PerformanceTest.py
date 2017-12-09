#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-8 下午3:24
# @Author  : sadscv
# @File    : PerformanceTest.py
import time
from threading import Thread
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25002))

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0

Thread(target=monitor).start()

while True:
    # start = time.time()
    sock.send(b'1')
    resp = sock.recv(100)
    # end = time.time()
    n += 1