#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-8 下午9:30
# @Author  : sadscv
# @File    : coroutine_fib.py
from collections import deque
from select import select
from socket import *

from multiThreading_Fibonacci.multiThreading_Fib import fib


tasks = deque()
recv_wait = {}
send_wait = {}
def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task = tasks.popleft()
        try:
            why, what = next(task)
            print(why, what)
            if why == 'recv':
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task

            else:
                raise RuntimeError("ARG!")
        except StopIteration:
            print("task done")



def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept()  #blocking
        print('Connection', addr)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        yield 'send', client
        client.send(resp)  # blocking
    print('Closed')
if __name__ == '__main__':
    tasks.append(fib_server(('', 25002)))
    run()