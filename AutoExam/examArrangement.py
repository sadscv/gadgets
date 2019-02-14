import logging
import os
import platform
import sqlite3
import sys
from datetime import datetime

import pandas as pd

# from AutoExam.converter import Converter
# from AutoExam.utils import

logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + '/log/arranger.txt',
                    filemode='a+',
                    format='%(asctime)-8s,%(msecs)d %(name)s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


class ExamArranger:
    def __init__(self, db_path=None):
        self.platform = platform.system()
        self.db = db_path
        self.conn, self.cursor = self.db_init()
        # self.preprocess()
        # self.exam_schedule()

    def preprocess(self):
        self._check_para()
        # self._check_kcYrs()
        self._course_select()
        self._drop_table('kcYrs')
        self._drop_table('xsYxk')
        self._drop_table('xsYkcms')

    def db_init(self):
        """
        init db connection, Win&&Linux supported
        :return: conn
        """
        if self.platform == 'Linux':
            print(self.db)
            conn = sqlite3.connect(self.db)
            # if debug
            conn.set_trace_callback(print)
            # converter = Converter(self.db)
            # converter.mdb2sqlite()
            # return converter.conn
            return conn, conn.cursor()
        elif self.platform == 'Windows':
            # Todo: update database config.
            user = ''
            password = ''
            odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" \
                            "DBQ=%s;UID=%s;PWD=%s" % (self.db, user, password)
            import pypyodbc
            conn = pypyodbc.connect(odbc_conn_str)
            return conn, conn.cursor()
        else:
            raise OSError('Unsupported OS')

    def _check_para(self):
        """
        check if Para table exist.
        if not exist: create Para table && add init value.
        :return: None
        """
        if not self._check_table("Para"):
            cur = self.conn.cursor()
            sql = "create table Para(ksxq datetime,A integer, B byte)"
            cur.execute(sql)
            sql = 'insert into Para values (#3/1/2004#,0,0)'
            cur.execute(sql)
            cur.close()
            self.conn.commit()
            return True

    def _check_table(self, table):
        cur = self.conn.cursor()
        if self.platform == 'Linux':
            sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table)
            if cur.execute(sql).fetchone():
                return True
        elif self.platform == 'Windows':
            if cur.tables(table=table, tableType='TABLE').fetchone():
                return True
            cur.close()
            return False

    # def _create_table(self, table, schema):
    #     """
    #
    #     :param table:
    #     :param schema: a list of tuple e.g. [(column_name, INTEGER),]
    #     :return:
    #     """
    #     cur = self.conn.cursor()
    #     # Todo: create table require columns to be defined
    #     sql = "CREATE TABLE {}();".format(table)
    #     cur.execute(sql)
    #     cur.close()

    def _delete_table(self, table):
        cur = self.conn.cursor()
        if self._check_table(table):
            cur.execute("drop table {}".format(str(table)))
            print('deleting table:{}'.format(table))

    def update_term(self):
        """
        update 'term' in Para table by given term value.
        :return:True/False
        """
        term = input('请输入本学期号:如(2019/3/1)')
        t = datetime.strptime(term, "%Y/%m/%d")
        sql = "update Para set ksxq='{}';".format(t)
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()
        self.conn.commit()
        return True

    def _course_select(self):
        """
        ' 课程号 选课人数 场次标识 不考试 语音室
        ' 266032    11 6	0	0
        ' 266115    15 16	0	0
        ' 266099    15 8	0	0
        ' 062313    15 22	0	0
        ' 266077    16 6	0	0
        :return: a table like this.
        """
        # Todo: warning. sql phrase is incomplete
        sql = "create table  kcYrs as " \
              "SELECT 学生与选课.课程号, Count(学生与选课.学号) AS 选课人数, 0 AS 场次标识 " \
              "FROM  学生与选课  " \
              "WHERE (((学生与选课.开课时间) = '09/01/18 00:00:00') And ((学生与选课.选课状态) = 0)) " \
              "GROUP BY 学生与选课.课程号 " \
              "ORDER BY Count(学生与选课.学号);"
        self._add_column('kcYrs', '不考试', 'bit')
        self._add_column('kcYrs', '语音室', 'bit')
        return True

    def exam_schedule(self):
        """
        :return:
        """
        # reset '场次标识' and '不考试' to default value
        self._reset_column('kcYrs', '场次标识', 0)
        self._reset_column('kcYrs', '不考试', False)
        exam_time = self.cursor.execute("select ksxq from Para")
        sql = "CREATE TABLE xsYxk if not exists AS " \
              "SELECT 学生与选课.课程号, 学生与选课.学号, 学生与选课.班级号 " \
              "FROM kcYrs INNER JOIN 学生与选课 ON kcYrs.课程号 = 学生与选课.课程号&  " \
              "WHERE (((学生与选课.开课时间) = {}) And ((学生与选课.选课状态) = 0) And ((kcYrs.不考试) = False))" \
              "ORDER BY 学生与选课.课程号, 学生与选课.学号;".format(exam_time)
        self.cursor.execute(sql)
        self._add_column('xsYxk', '序号', 'Byte')
        self._add_column('xsYxk', '座位号', 'Byte')
        self._reset_column('xsYxk', '序号', 1)
        # create xsYkcms[学生与课程门数]
        sql = "CREATE TABLE xsYkcms AS " \
              "SELECT xsYxk.学号, Count(xsYxk.课程号) AS 选课门数 " \
              "FROM xsYxk GROUP BY xsYxk.学号;"
        self.cursor.execute(sql)
        # 所有要排考的课程门数
        course_count = self._select_count('kcYrs', "'不考试'=False", '课程号')
        # 非公选课门数=> 课程号!='00*'
        nonpub_count = self._select_count('kcYrs', "'不考试'=False and '课程号' not like '00*'", '课程号')

    def _reset_column(self, table, column, value):
        """
        # Todo: abstract this func to api
        :return:
        """
        cur = self.conn.cursor()
        sql = "update {} set {} = {};".format(table, column, value)
        cur.execute(sql)
        cur.close()

    def _drop_table(self, table):
        if self._check_table(table):
            cur = self.conn.cursor()
            sql = "drop Table {}".format(table)
            cur.execute(sql)
            self.conn.commit()

    def _add_column(self, table, column, field_type):
        cur = self.conn.cursor()
        sql = "PRAGMA TABLE_INFO({})".format(table)
        columns = [r[1] for r in cur.execute(sql)]
        if column not in columns:
            sql = "alter table {} add column {} {};".format(table, column, field_type)
            cur.execute(sql)
            self.conn.commit()
            return True
        else:
            logger.warning('column:{} already existed in table{}'.format(column, table))
            return False

    def _select_count(self, table, criteria=None, column='*'):
        """
        :param table: table name
        :param criteria: criteria for the selection
        :param column: column to be count
        :return: Count of affected rows by given SELECT criteria
        """
        cur = self.conn.cursor()
        if criteria:
            sql = "select count({}) from {} where {};".format(column, table, criteria)
        else:
            sql = "select count({}) from {};".format(column, table)
        cur.execute(sql)
        # cur.fetchall()[0]
        return cur.fetchone()[0]


def empty_room(conn):
    query = "SELECT * FROM 历届十佳 where ID=2;"
    data = pd.read_sql(query, conn)
    print(data)


if __name__ == '__main__':
    # filepath = r'''C:\Users\sadscv\Desktop\考试安排测试.accdb'''
    filepath = sys.argv[1]
    arranger = ExamArranger(db_path=filepath)
    arranger.update_term(arranger.cursor)
    # testTable('历届百佳',conn.cursor())
