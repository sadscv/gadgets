from datetime import datetime

import pypyodbc as pypyodbc
import pandas as pd

from AutoExam.utils import testTable

def connectDB():
    """
    connect Access database
    :return:connection
    """
    db_file = r'''C:\Users\sadscv\Desktop\考试安排测试.accdb'''
    #Todo update database config.
    user = ''
    password = ''
    odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;UID=%s;PWD=%s"%(db_file, user, password)
    conn = pypyodbc.connect(odbc_conn_str)
    return conn


def empty_clsroom(conn):
    query = "SELECT * FROM 历届十佳 where ID=2;"
    data = pd.read_sql(query,conn)
    print(data)

def init():
    """
    init database connection.
    check if Para table exist.
    :return: conn
    """
    conn = connectDB()
    cursor = conn.cursor()
    if not testTable("Para", cursor):
        str = "create table Para(ksxq datetime,A integer, B byte)"
        cursor.execute(str)
    str = 'insert into Para values (#3/1/2004#,0,0)'
    cursor.execute(str)
    conn.commit()
    return conn


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
    conn = init()
    update_para(conn.cursor())
    # testTable('历届百佳',conn.cursor())

