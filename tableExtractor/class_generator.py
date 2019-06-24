#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: sadscv
@time: 2019/6/21 15:07
@file: class_generator.py
@desc:
"""
import pyodbc
import re

import openpyxl as openpyxl
from openpyxl import Workbook


class CONFIG:
    input_path = "docs/江西师范大学2019年本科招生计划一览表（530定）.xlsx"
    output_path = "docs/output.xlsx"
    old_campus_list = ['音乐学', '音乐表演', '舞蹈学', '表演(健美操方向）',
                       '表演（体育舞蹈方向）', '武术与民族传统体育']


class ClassGenerator:
    def __init__(self):
        self.processed_lines = []
        self.count = 0
        self.config = CONFIG()

    def read_raw(self):
        raw_xls = openpyxl.load_workbook(self.config.input_path)
        print(raw_xls.sheetnames)
        ws = raw_xls.active
        for row in ws.iter_rows(min_row=2, max_row=105):
            major_name = str(row[1].value)
            # test case1：汇总一行为空
            if major_name != '汇总':
                # for each line in excel, loop i time while i is the number of
                # classes of current major
                self.read_line(row, major_name)

    def read_line(self, row, major_name):
        major_population = int(row[13].value)
        processed_line = {}
        for i in range(int(row[16].value)):
            class_population = major_population // (int(row[16].value) - i)
            major_population -= class_population
            tmp = re.match('[\u4e00-\u9fa5]', major_name)
            major_name = major_name[:tmp.endpos]
            tmp1 = re.search('类|S|J', major_name)

            # if class_name contain 类 or S or J, we have to remove it
            if tmp1:
                major_name = major_name[:tmp1.span()[0] + 1]
                if major_name[-1:] != '类':
                    major_name = major_name[:-1]

            # if current major has only one class, we don't need to
            # append class_number after the major name.
            if int(row[16].value) == 1:
                self.count += 1
                class_name = "19级{}班".format(major_name)
            else:
                self.count += 1
                class_name = "19级{}{}班".format(major_name, i + 1)
            processed_line['班级号'] = self.count
            processed_line['班级名称'] = class_name
            processed_line['班级性质号'] = '01'
            processed_line['年级号'] = '2019/9/1'
            processed_line['班级人数'] = class_population
            processed_line['学分制状态'] = '1'
            if major_name in self.config.old_campus_list:
                processed_line['教学区号'] = '01'
            else:
                processed_line['教学区号'] = '02'
            self.processed_lines.append(processed_line)
        print('1')

    def write2xls(self):
        wb = Workbook()
        ws = wb.active
        ws['A1'] = '班级号'
        for item in range(len(self.processed_lines)):
            print(item)


        # wb.save(self.config.output_path)


if __name__ == '__main__':
    cg = ClassGenerator()
    cg.read_raw()
    cg.write2xls()
