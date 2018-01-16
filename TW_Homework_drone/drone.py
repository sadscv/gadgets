#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-16
# @Author  : sadscv
# @File    : drone.py

class Drone(object):
    def __init__(self):
        self.valid = True
        self.paths = [] # 假设每秒回传一次，根据无人机目前<30min 的续航，数量级下不会有性能问题。

    def create_path(self, pos):
        self.pos = pos
        def drone_path(offset): # path_writer
            ## Todo 判断参数合法性，生成坐标合法性
            pos[0] += offset[0]
            pos[1] += offset[1]
            pos[2] += offset[2]
            return pos
        return drone_path

    def invalid(self):
        self.valid = False







if __name__ == '__main__':
    drone = Drone()
    path = drone.create_path(pos=[1,2,3])
    print(drone.pos)

