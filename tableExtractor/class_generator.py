#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: sadscv
@time: 2019/6/21 15:07
@file: class_generator.py
@desc:
"""
import openpyxl as openpyxl


class CONFIG:
    input_path = "docs\江西师范大学2019年本科招生计划一览表（530定）.xlsx"


class ClassGenerator():
    def __init__(self):
        self.config = CONFIG()

    def read_raw(self):
        raw_xls = openpyxl.load_workbook(self.config.input_path)
        print(raw_xls.sheetnames)
        ws = raw_xls.active
        for row in ws.iter_rows(min_row=4):
            class_name = str(row[1].value)
            if class_name != '汇总':
                for i in range(int(row[16].value)):
                    index = 0
                    char = class_name[0]
                    print(char)
                    while ClassGenerator.is_chinese(char):
                        index += 1
                        char = class_name[index]
                    class_name = class_name[:index]
                    print(class_name)
                    # print("19级{}{}班".format(row[1].value, i))

    @staticmethod
    def is_chinese(word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False


if __name__ == '__main__':
    cg = ClassGenerator()
    cg.read_raw()
