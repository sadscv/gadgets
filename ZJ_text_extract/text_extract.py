#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-18
# @Author  : sadscv
# @File    : textExtract.py
import re


def savelines(line=None, file=None):
    pass

def readfile():
    SAVE = None
    with open('data/trainSessionDeepMedic.txt','r') as f:
        tmpfile = open('data/Epoch.txt', 'wb')
        # split file
        for line in f:
            print(SAVE)
            head = re.search('Starting new Epoch! Epoch', line, flags=0)
            if head:
                pos = re.search('#', line).span()[1]
                num = line[pos:pos+2].rstrip('/')
                SAVE = num
                open('data/Epoch_{}.txt'.format(SAVE), 'wb')
                tmpfile = open('data/Epoch_{}.txt'.format(SAVE), 'a')
                # savelines(file=tmpfile)
                # tmpfile.close()
            elif SAVE:
                tmpfile.write(line)
                # with open('data/Epoch_{}.txt'.format(SAVE), 'a') as subf:
                #     subf.write(line)

        # read sub_file


def subfileExtract(epoch):
    with open('data/Epoch_{}.txt'.format(epoch), 'r') as f:
        classJson = []
        for line in f:
            if re.search('finished. Reporting Accuracy over whole epoch.', line):
                tmp = []
                for i in range(4):
                    currentLine = next(f)
                    if re.search('VALIDATION', currentLine):
                        tmp.append(currentLine)
                classJson.append(JSONGenerater(tmp, 'whole'))
            if re.search('Reporting Accuracy over whole epoch for Class', line):
                tmpval = []
                tmptrain = []
                # Todo 添加函数，重构重复代码。
                for i in range(8):
                    currentLine = next(f)
                    if re.search('VALIDATION', currentLine):
                        tmpval.append(currentLine)
                    if re.search('TRAINING', currentLine):
                        tmptrain.append(currentLine)
                    classJson.append(JSONGenerater(tmpval, 'validation'))
                    classJson.append(JSONGenerater(tmptrain, 'training'))
                for t in tmptrain:
                    print(t)



def JSONGenerater(lines, flag=None):
    # 送进来8行，输出一个json. 代表epoch*-validation(or training)-class* 包含的数据
    # 如果长度为2，则是overall validation

    pass





if __name__ == '__main__':
    # readfile()
    subfileExtract(1)