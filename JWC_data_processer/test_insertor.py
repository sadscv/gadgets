#!/usr/bin/env python
# encoding : utf-8
# @Time    : 19-4-17 上午10:43
# @File    : classname_insert.py
# @Author  : sadscv

from unittest import TestCase

from JWC_data_processer.classname_insert import class_insertor


class TestInsertor(TestCase):
    def setUp(self):
        self.teacher_list = ['jwc046']
        self.insertor = class_insertor()
        self.conn, self.cursor = self.insertor.db_init()

    def tearDown(self):
        pass

    def test_db_init(self):
        self.insertor.db_init()

    def test_get_course_info_by_t_id(self):
        for t in self.teacher_list:
            class_info = self.insertor.get_course_info_by_t_id(
                cursor=self.cursor, t_id=t)
            print(len(class_info))

    def test_insert_course_name(self):
        pass
