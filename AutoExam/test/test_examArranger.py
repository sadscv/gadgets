#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: sadscv
@time: 2019/02/13 14:10
@file: test_examArranger.py

@desc: 
"""
from unittest import TestCase
from unittest.mock import patch

from AutoExam.examArrangement import ExamArranger


class TestExamArranger(TestCase):
    def setUp(self):
        db_path = '/home/sadscv/PycharmProjects/gadgets/AutoExam/data/201811210[19:50].sqlite'
        self.arranger = ExamArranger(db_path)
        self.cur = self.arranger.conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS  tmp_test(rowid INTEGER PRIMARY KEY );"
        self.cur.execute(sql)

    def tearDown(self):
        sql = "drop table if exists tmp_test "
        self.cur.execute(sql)
        self.arranger.conn.close()

    def test_preprocess(self):
        pass

    def test_db_init(self):
        """
        nothing to test
        :return:
        """
        self.platform = ''
        self.assertRaises(OSError)

    def test_check_table(self):
        self.assertTrue(self.arranger._check_table('tmp_test'))
        self.arranger._delete_table('tmp_test')
        self.assertFalse(self.arranger._check_table('tmp_test'))

    def test_delete_table(self):
        """
        already tested by case 'test_check_table'
        :return:
        """
        pass

    def test__check_para(self):
        cur = self.arranger.conn.cursor()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='Para';"
        self.assertTrue(cur.execute(sql).fetchone())
        cur.close()

    @patch('builtins.input', side_effect=['2019/3/1'])
    def test_update_term(self, mocked_input):
        cur = self.arranger.conn.cursor()
        self.arranger.update_term()
        sql = 'select ksxq as "[timestamp]" from Para;'
        # Todo :将数据库中的datetime转换成相应格式测试
        import datetime
        fmt_db = '%Y-%m-%d %H:%M:%S'
        fmt = '%Y/%m/%d'
        result = datetime.datetime.strptime(cur.execute(sql).fetchone()[0], fmt_db)
        raw = datetime.datetime.strptime('2019/3/1', fmt)
        self.assertEqual(result, raw)

    def test__course_select(self):
        self.fail()

    def test_exam_schedule(self):
        self.fail()

    def test__reset_column(self):
        self.arranger._add_column('tmp_test', 'test_column', 'INTEGER')
        sql = "insert into tmp_test (test_column) VALUES (0);"
        self.cur.execute(sql)
        self.assertNotEqual(self.cur.execute(sql), 1)
        self.arranger._reset_column('tmp_test', 'test_column', 1)
        sql = "select test_column from tmp_test limit 1;"
        self.cur.execute(sql)
        self.assertEqual(self.cur.execute(sql).fetchone()[0], 1)

    def test__drop_table(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='tmp_test';"
        self.assertTrue(self.cur.execute(sql).fetchone())
        self.arranger._drop_table('tmp_test')
        self.assertFalse(self.arranger._check_table('tmp_table'))

    def test__add_column(self):
        self.arranger._add_column('tmp_test', 'test_column', 'INTEGER')
        sql = "PRAGMA TABLE_INFO(tmp_test);"
        columns = [r[1] for r in self.cur.execute(sql)]
        self.assertIn('test_column', columns)

    def test__select_count(self):
        for i in range(100):
            sql = "INSERT INTO tmp_test (rowid) VALUES ({});".format(i)
            self.cur.execute(sql)
        self.assertEqual(self.arranger._select_count(table='tmp_test', column='rowid'), 100)

