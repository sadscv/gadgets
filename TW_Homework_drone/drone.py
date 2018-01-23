#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-16
# @Author  : sadscv
# @File    : drone.py
import os
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='./log/drone.txt')
logger.setLevel(logging.INFO)

class Drone(object):
    def __init__(self, filepath=None):
        # logger.info('======program starting======')
        self.working = True
        self.id = None
        self.pos = [0, 0, 0]
        self.paths = []
        self.lineidx = -1
        if filepath:
            try:
                self.filepath = filepath
                self.readfile(self.filepath)
            except FileNotFoundError as e:
                logger.error(e)
                logger.error('file not found, check the filename and path')
                sys.exit(1)


    def fly(self, offset):
        # path_writer, add offset to current position

        assert len(self.pos) == len(offset)
        for i in range(len(offset)):
            self.pos[i] += offset[i]


    def readfile(self, filepath):
        # 将每一行验证后加入当前轨迹
        with open(filepath, 'r') as f:
            logger.info('loading file')
            for line in f:  # 如果这一行OK，那么就将其加入轨迹记录。
                self.lineidx += 1
                if self.working and self.valid_signal(line):
                    logger.info('validating:{},result:{}'.format(line.strip(), True))
                    self.paths.append(tuple(self.pos))
                else:
                    logger.info('validating:{},result:{}'.format(line.strip(), False))
                    self.paths.append(('NA', 'NA', 'NA'))
                    self.working = False
            return self.working

    def valid_signal(self, signal):
        sigList = [str(s) for s in signal.split()]

        # Case1:the drone first time appear in aera, length of signal == 4
        if len(sigList) == 4 and self.id is None:
            # Case1.1/Case1.2  if matched,return true
            if sigList[0].isalnum() and all(self.is_digit(s) for s in sigList[1:]):
                self.id = sigList[0]
                self.fly([int(s) for s in sigList[1:]])
                return True
            else:  # Case 1.3 if not matched,return False
                logger.error('名字需由数字和字母组成')

        # Case2: drone is not first seen in aera, and length of singal == 7
        elif len(sigList) == 7 and self.id:
            # valid drone.id to see if it's the same drone, and check left parameters
            if sigList[0] == self.id and all(self.is_digit(s) for s in sigList[1:]):
                prev_pos = [float(i) for i in sigList[1:4]]
                # if previous position matched, add current offset as drone's next step
                isMatch = all(prev_pos[i] == self.pos[i] for i in range(len(self.pos)))
                if isMatch:  # 如果之前的状态match
                    self.fly([float(j) for j in sigList[4:7]])
                    return True

        # some bad Cases
            elif sigList[0] == self.id:
                logger.error('line:{}, 参数错误，不合法'.format(self.lineidx))
            else:
                logger.error('line:{}, 名字不相等'.format(self.lineidx))
        elif len(sigList) == 4 and self.id:  # 长度为4，但是已经有id
            logger.error('line:{}, 长度为4，但是已经有id'.format(self.lineidx))
        elif len(sigList) == 7 and self.id is None:  # 长度为7，但没id
            logger.error('line:{}, 长度为7，但没id'.format(self.lineidx))
        else:  # 长度不符合
            logger.error('line:{}, 长度不符合'.format(self.lineidx))
        return False

    @staticmethod
    def is_digit(num, int_only=True):
        #  Check if a Number is Positive, Negative or 0 判断一个数是否符合正整数，负整数，0的范畴
        #  return:
        #  True: 1, -1, 0, 1.00, -1.00, 0.00
        #  False: abc123, 1.1111,
        # 区别 int_only
        if int_only:
            return str(num).lstrip('-').isdigit()
        try:
            f_num = float(num)
            i_num = int(f_num)
            if f_num != i_num:
                return False
        except ValueError as e:
            return False
        else:
            return True

    def check(self, line):
        '''

        :param line:
        :return: Flase:行数不合法; -1:out of range;  0:'NA,NA,NA'; other:(int,int,int)
        '''
        if not str(line).isdigit():
            return 'invalid input'
        if int(line) >= len(self.paths):
            return 'cannot find {}'.format(line)
        if self.paths[int(line)] == ('NA', 'NA', 'NA'):
            return 'Error: {}'.format(line)
        # pretty print: result before (1.00,1.23, 0.00), result after(1, 1.23, 0)
        result = [self.id, line] + [int(n) for n in self.paths[int(line)] if int(n) == float(n)]
        return ' '.join(map(str, result))



if __name__ == '__main__':
    try:
        drone = Drone(filepath=sys.argv[1])
    except IndexError:
        print('filepath required')
        sys.exit(1)

    while True:
        inputs = input('enter a number:')
        result = drone.check(inputs)
        print(result)

        # print(Drone.is_digit(-1.0, int_only=True))

