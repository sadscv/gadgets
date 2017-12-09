#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-8 下午8:07
# @Author  : sadscv
# @File    : multiProcessing_fib.py

from socket import *
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool
from multiThreading_Fibonacci.multiThreading_Fib import fib

pool = Pool(4)

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        result = future.result()
        # result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('Closed')



def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connection', addr)
        Thread(target=fib_handler, args=(client,), daemon=True).start()


if __name__ == '__main__':
    fib_server(('', 25002))