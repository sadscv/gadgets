#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-1-25 上午10:43
# @File    : getDepartureTime.py

import json
import requests


# 以下代码用于代理，如不需要可删除。
# 此代码属半成品，需重写get_time方法。
import socket
import socks

socks.set_default_proxy(socks.HTTP, "138.201.63.123", 31288)
socket.socket = socks.socksocket


class DepartureTimer:

    def __init__(self, url):
        self.url = url

    def get_raw(self, url):
        raw = None
        try:
            raw = json.loads(requests.get(url).text)
        except requests.Timeout as e:
            print(e)
        return raw

    def get_routes(self):
        routes = []
        raw = self.get_raw(self.url + 'Routes' + url_format)
        print('which bus route are you taking?')
        for r in raw:
            if r['Route']:
                routes.append(r['Route'])
        return routes

    def get_directions(self, route):
        raw = self.get_raw(self.url + 'Directions/' + route + url_format)
        print(
            'which direction are you travelling on route %s? (Enter number)' %
            route)
        directions = []
        for r in raw:
            if r['Value'] and r['Text']:
                print('%s for %s' % (r['Value'], r['Text']))
                directions.append(r['Value'])
        return directions

    def get_stops(self, route, direction):
        raw = self.get_raw(self.url + 'Stops/' + route + '/' + direction +
                          url_format)
        stops = []
        print('Which stop will you depart from? (Enter stop code)')
        for r in raw:
            if r['Value'] and r['Text']:
                print('%s for %s' % (r['Value'], r['Text']))
                stops.append(r['Value'])
        return stops

    def get_time(self, route, direction, stop):
        raw = self.get_raw(self.url + route + '/' + direction + '/'
                           + stop + url_format)
        # todo 从此处继续
        if raw:
            for r in raw:
                print(r)
        else:
            print('shit, empty')

    @staticmethod
    def verified_input(options):
        opt = input()
        while opt not in options:
            print('invalid input, try again')
            opt = input()
        return opt


url = 'http://svc.metrotransit.org/NexTrip/'
url_format = '?format=json'

if __name__ == '__main__':
    DT = DepartureTimer(url)
    route = DT.verified_input(DT.get_routes())
    direction = DT.verified_input(DT.get_directions(route))
    stop = DT.verified_input(DT.get_stops(route, direction))
    DT.get_time(route, direction, stop)
