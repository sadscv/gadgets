#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-4-17 上午10:43
# @File    : classname_insert.py
# @Author  : sadscv
import platform
import sqlite3


def db_init(self, db_path=None):
    """
    init db connection, Win&&Linux supported
    :return: conn
    """
    my_platform = platform.system()
    if my_platform == 'Linux':
        conn = sqlite3.connect(db_path)
        conn.set_trace_callback(print)
        # converter = Converter(self.db)
        # converter.mdb2sqlite()
        # return converter.conn
        return conn, conn.cursor()
    elif my_platform == 'Windows':
        # Todo: update database config.
        user = ''
        password = ''
        odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" \
                        "DBQ=%s;UID=%s;PWD=%s" % (db_path, user, password)
        import pypyodbc
        conn = pypyodbc.connect(odbc_conn_str)
        return conn, conn.cursor()
    else:
        raise OSError('Unsupported OS')


def insert_course_name(teacher_list):
    conn, cursor = db_init()
    # 班级号、班级名称、班级性质号、年级号、班级人数、学分制状态、辅导员信息、开课时间、备注
    # 教学区号、教材费结余
    sql = "insert into 班级 values ('{}','{}','{}',,,'{}',,,,,);".format(
        init_time)


if __name__ == '__main__':
    teacher_list = []
    insert_course_name(teacher_list)
