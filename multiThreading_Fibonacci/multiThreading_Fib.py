#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-12-8 下午3:21
# @Author  : sadscv
# @File    : Fibonacci.py

from socket import *
from threading import Thread

def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def fib_handler(client):
    '''
    来了一个client， 先取得他的request，如果取不到则路过循环，取到了就拿给fib(n)计算并返回结果
    返回时应将结果转成字符串方便传输
    :param client: <client>
    :return: <str>
    '''
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print('Closed')

def fib_server(address):
    '''
    来了一个http请求进来，那么sock就会将其接收作为一个client，再将client交给fib_handler处理
    :param address:
    :return:
    '''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connection', addr)
        # 单线程版本
        # fib_handler(client)
        # 多线程版本
        Thread(target=fib_handler, args=(client,), daemon=True).start()


if __name__ == '__main__':
    fib_server(('',25002))