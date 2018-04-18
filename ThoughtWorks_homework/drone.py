#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-16
# @Author  : sadscv
# @File    : drone.py
import os
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename= os.path.dirname(os.path.abspath(__file__))+'/log/drone_log.txt',
                            filemode='a',
                            format='%(asctime)-8s,%(msecs)d %(name)s %(levelname)-8s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

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
                self.read_file(self.filepath)
            except FileNotFoundError as e:
                logger.error('file not found, check the filename and path<==== line:{}'.format(self.lineidx))
                sys.exit(1)


    def _fly(self, offset):
        # path_writer, add offset to current position
        assert len(self.pos) == len(offset)

        for i in range(len(offset)):
            self.pos[i] += offset[i]


    def read_file(self, filepath):
        # # check every line in file
        with open(filepath, 'r') as f:
            logger.info('loading file')
            for line in f:
                self.lineidx += 1
                if self.working and self.valid_signal(line): # if self.working, add current position to paths
                    logger.info('validating:{},result:{}<==== line:{}'.format(line.strip(), True, self.lineidx))
                    self.paths.append(tuple(self.pos))
                else: # if self.working==False, add 'NA' to paths
                    logger.info('validating:{},result:{}<==== line:{}'.format(line.strip(), False, self.lineidx))
                    self.paths.append(('NA', 'NA', 'NA'))
                    self.working = False
            return self.working

    def valid_signal(self, signal):
        '''

        :param signal: str compose by 4 or 7 elements, e.g. 'plane1 1 1 1 1 2 3'
        :return:Bool  if signal is valid or not
        '''
        sigList = [str(s) for s in signal.split()]

        # Case1:the drone first time appear in aera, length of signal == 4
        if len(sigList) == 4 and self.id is None:
            # Case1.1/Case1.2  if matched,return true
            if sigList[0].isalnum() and all(self.is_digit(s) for s in sigList[1:]):
                self.id = sigList[0]
                self._fly([int(s) for s in sigList[1:]])
                return True
            else:  # Case 1.3 if not matched,return False
                logger.error('name should compose by integers and alphabets <==== line:{}'.format(self.lineidx))

        # Case2: drone is not first seen in aera, and length of singal == 7
        elif len(sigList) == 7 and self.id:
            # valid drone.id to see if it's the same drone, and check left parameters
            if sigList[0] == self.id and all(self.is_digit(s) for s in sigList[1:]):
                prev_pos = [float(i) for i in sigList[1:4]]
                # if previous position matched, add current offset as drone's next step
                isMatch = all(prev_pos[i] == self.pos[i] for i in range(len(self.pos)))
                if isMatch:
                    self._fly([float(j) for j in sigList[4:7]])
                    return True

        # some bad Cases
            elif sigList[0] == self.id:
                logger.error('parameter is invalid <==== line:{}'.format(self.lineidx))
            else:
                logger.error('name is not matched line:{}'.format(self.lineidx))
        elif len(sigList) == 4 and self.id:
            logger.error('length is 4 but not first appear in area <==== line:{}'.format(self.lineidx))
        elif len(sigList) == 7 and self.id is None:
            logger.error('length is 7 but first apprear <==== line:{}'.format(self.lineidx))
        else:
            logger.error('length is invalid <==== line:{}'.format(self.lineidx))
        return False

    @staticmethod
    def is_digit(num, int_only=True):
        '''
         Check if a Number is Positive, Negative or 0
         if int_only==True:     is_digit(1.0) == False
         if int_only==Flase:    is_digit(1.0) == True

        :param num: num or num like str
        :param int_only:
        :return: True/False
        '''

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
        check if a line is okay
        :param line: int or int like str
        :return: if everything ok : return
        '''
        if not str(line).isdigit(): # check if is valid
            return 'invalid input'

        if int(line) >= len(self.paths): # check if out of range
            return 'cannot find {}'.format(line)

        if self.paths[int(line)] == ('NA', 'NA', 'NA'): # check if result is 'NA'
            return 'Error: {}'.format(line)
        # pretty print: result before (1.00,1.23, 0.00), result after(1, 1.23, 0)
        result = [self.id, line] + [int(n) for n in self.paths[int(line)] if int(n) == float(n)]
        logger.info('Check line: result:{} <==== line:{}'.format(result, line))
        return ' '.join(map(str, result))


if __name__ == '__main__':
    try:
        drone = Drone(filepath=sys.argv[1])
    except IndexError:
        print('filepath argment required but missing')
        sys.exit(1)

    while True:
        inputs = input('enter a num: ==> ')
        result = drone.check(inputs)
        print(result)
