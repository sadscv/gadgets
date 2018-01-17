#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-16
# @Author  : sadscv
# @File    : drone.py

class Drone(object):
    def __init__(self, path):
        self.valid = True
        self.id = None
        self.path = path
        self.paths = []  # 假设每秒回传一次，根据无人机目前<30min 的续航，数量级下不会有性能问题。
        self.pathManger = self.create_path()
        self.input_file(path=self.path)

    def create_path(self, pos=[0,0,0]):
        self.pos = pos
        def drone_path(offset):  # path_writer
            for i in range(3):
                self.pos[i] += offset[i]
            return pos
        return drone_path

    def input_file(self, path='file.txt'):
        # 将每一行验证后加入当前轨迹
        with open(path, 'r') as f:
            for line in f:  # 如果这一行OK，那么就将其加入轨迹记录。
                if self.valid_status(line):
                    self.paths.append(tuple(self.pos))
                else:
                    self.paths.append(('NA', 'NA', 'NA'))
                    self.valid = False

    def valid_status(self, signal):
        print(self.id, self.pos)
        sigList = [str(s) for s in signal.split()]

        if len(sigList) == 4 and self.id is None:  # valid if it's the debut on area first time occur #Todo 验证debut正确与否
            if sigList[0].isalnum():
                self.id = sigList[0]
            else:
                print('名字需由数字和字母组成')
                return False
            is_digits = all(self.isDigit(s) for s in sigList[1:])
            if is_digits:
                self.pathManger([float(s) for s in sigList[1:]])
                print('ok,路径修改成功')
                return True

        elif len(sigList) == 7 and self.id:  # valid if the status is ok
            if sigList[0] == self.id:
                # Todo 验证[4,7]是否为浮点数
                pre_pos = [float(i) for i in sigList[1:4]]
                isMatch = all(pre_pos[i] == self.pos[i] for i in range(3))
                if isMatch:  # 如果之前的状态match
                    after_pos = [float(j) for j in sigList[4:7]]
                    self.pathManger(after_pos)
            else:
                print('名字不相等')
        elif len(sigList) == 4 and self.id:  # 长度为4，但是已经有id
            print('长度为4，但是已经有id')
            return False
        elif len(sigList) == 7 and self.id is None:  # 长度为7，但没id
            print('长度为7，但没id')
            return False
        else:  # 长度不符合
            return False

    @classmethod
    def isDigit(self, num):
        #  Check if a Number is Positive, Negative or 0 判断一个数是否符合正整数，负整数，0的范畴
        #  return:
        #  True: 1, -1, 0, 1.00, -1.00, 0.00
        #  False: abc123, 1.1111,
        try:
            f_num = float(num)
            i_num = int(f_num)
            if f_num != i_num:
                return False
        except ValueError as e:
            return False
        else:
            return True


if __name__ == '__main__':
    FILEPATH = './file.txt'
    drone = Drone(path=FILEPATH)
