from datetime import datetime

import pypyodbc
import pandas as pd

from AutoExam.utils import testTable, delete_table


class ExamArranger():
    def __init__(self, db_file=None):
        self.db_file = db_file
        self.conn = self.connectDB(db_path=db_file)
        self.cursor = self.conn.cursor()
        self.check_para()

    def connectDB(self, db_path):
        """
        connect Access database
        :return:connection
        """
        #Todo update database config.
        user = ''
        password = ''
        odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;UID=%s;PWD=%s"%(self.db_file, user, password)
        conn = pypyodbc.connect(odbc_conn_str)
        return conn

    def check_para(self):
        if not testTable("Para", self.cursor):
            str = "create table Para(ksxq datetime,A integer, B byte)"
            self.cursor.execute(str)
            str = 'insert into Para values (#3/1/2004#,0,0)'
            self.cursor.execute(str)
            self.conn.commit()

def empty_clsroom(conn):
    query = "SELECT * FROM 历届十佳 where ID=2;"
    data = pd.read_sql(query,conn)
    print(data)


def update_para(cursor=None):
    """
    update term from default value to current term.
    :param cursor:
    :return:True/False
    """
    try:
        term = input('请输入本学期号:')
        str = "update Para set ksxq=#{}#".format(term)
        cursor.execute(str)
        cursor.commit()
        return True
    except:
        pass


if __name__ == '__main__':
    db_file = r'''C:\Users\sadscv\Desktop\考试安排测试.accdb'''
    arranger = ExamArranger(db_file=db_file)
    update_para(arranger.cursor())
    # testTable('历届百佳',conn.cursor())

