import os
import platform
import sqlite3
import sys
from datetime import datetime, time

import pandas as pd

from AutoExam.converter import Converter
from AutoExam.utils import testTable, delete_table


class ExamArranger:
    def __init__(self, db_path=None):
        self.db = db_path
        self.platform = platform.system()
        self.conn = self.db_init()
        # self.conn = self.connectDB(db_path=db_path)
        self.cursor = self.conn.cursor() # only for func Para delivery
        self._check_para()

    def db_init(self):
        """
        :return: conn
        """
        if self.platform == 'Linux':
            conn = sqlite3.connect(sys.argv[1])
            # if debug
            conn.set_trace_callback(print)
            # converter = Converter(self.db)
            # converter.mdb2sqlite()
            # return converter.conn
            return conn
        elif self.platform == 'Windows':
            # Todo: update database config.
            user = ''
            password = ''
            odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" \
                            "DBQ=%s;UID=%s;PWD=%s" % (self.db, user, password)
            import pypyodbc
            conn = pypyodbc.connect(odbc_conn_str)
            return conn
        else:
            raise OSError('Unsupported OS')

    def _check_para(self):
        if not testTable("Para", self.cursor, platform=self.platform):
            cur = self.conn.cursor()
            sql = "create table Para(ksxq datetime,A integer, B byte)"
            cur.execute(sql)
            sql = 'insert into Para values (#3/1/2004#,0,0)'
            cur.execute(sql)
            cur.close()
            self.conn.commit()

    def _update_para(self):
        """
        update term from default value to current term.
        :return:True/False
        """
        term = input('请输入本学期号:')
        t = datetime.strptime(term, "%Y/%m/%d")
        sql = "update Para set ksxq='{}';".format(t)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return True


def empty_room(conn):
    query = "SELECT * FROM 历届十佳 where ID=2;"
    data = pd.read_sql(query, conn)
    print(data)


if __name__ == '__main__':
    # filepath = r'''C:\Users\sadscv\Desktop\考试安排测试.accdb'''
    filepath = sys.argv[1]
    arranger = ExamArranger(db_path=filepath)
    arranger._update_para(arranger.cursor)
    # testTable('历届百佳',conn.cursor())
