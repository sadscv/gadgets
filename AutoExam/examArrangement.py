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
                    datefmt='%d/%m/%y %H:%M:%S',
                    level=logging.INFO)


class ExamArranger:
    def __init__(self, db_path=None):
        self.platform = platform.system()
        self.db = db_path
        self.conn, self.cursor = self.db_init()
        self._check_para()
        self.exam_time = self.cursor.execute("select ksxq from Para").fetchone()[0]
        # self.preprocess()
        # self.exam_schedule()
        # self.course_schedule()

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
            sql = "create table if not exists  Para(ksxq datetime,A integer, B byte);"
            cur.execute(sql)
            init_time = datetime.strptime('3/1/04', "%m/%d/%y").strftime('%m/%d/%y %H:%M:%S')
            sql = "insert into Para values ('{}', 0, 0);".format(init_time)
            cur.execute(sql)
            cur.close()
            self.conn.commit()
            return True

    def _check_table(self, table):
        cur = self.conn.cursor()
        if self.platform == 'Linux':
            sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(table)
            try:
                if cur.execute(sql).fetchone():
                    return True
            except Exception:
                pass
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
        t = datetime.strptime(term, "%Y/%m/%d").strftime('%m/%d/%y %H:%M:%S')
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
        cur = self.conn.cursor()
        sql = "create table if not exists kcYrs as " \
              "SELECT 学生与选课.课程号 AS 课程号, Count(学生与选课.学号) AS 选课人数, 0 AS 场次标识 " \
              "FROM  学生与选课  " \
              "WHERE (((学生与选课.开课时间) = '09/01/18 00:00:00') And ((学生与选课.选课状态) = 0)) " \
              "GROUP BY 学生与选课.课程号 " \
              "ORDER BY Count(学生与选课.学号);"
        cur.execute(sql)
        self._add_column('kcYrs', '不考试', 'bit')
        self._add_column('kcYrs', '语音室', 'bit')
        return True

    def exam_schedule(self):
        """
        :return:
        """
        # reset '场次标识' and '不考试' to default value
        self._reset_column('kcYrs', '场次标识', 1)
        self._reset_column('kcYrs', '不考试', 0)
        print(self.exam_time)
        sql = "CREATE TABLE if not exists xsYxk AS " \
              "SELECT 学生与选课.课程号, 学生与选课.学号, 学生与选课.班级号 " \
              "FROM kcYrs INNER JOIN 学生与选课 ON kcYrs.课程号 = 学生与选课.课程号 " \
              "WHERE (((学生与选课.开课时间) = '{}') And ((学生与选课.选课状态) = 0) And ((kcYrs.不考试) = 0))" \
              "ORDER BY 学生与选课.课程号, 学生与选课.学号;".format(self.exam_time)
        self.cursor.execute(sql)
        self._add_column('xsYxk', '序号', 'Byte')
        self._add_column('xsYxk', '座位号', 'Byte')
        self._reset_column('xsYxk', '序号', 1)
        # create xsYkcms[学生与课程门数]
        sql = "CREATE TABLE if not exists xsYkcms AS " \
              "SELECT xsYxk.学号, Count(xsYxk.课程号) AS 选课门数 " \
              "FROM xsYxk GROUP BY xsYxk.学号;"
        self.cursor.execute(sql)
        # 所有要排考的课程门数 number of courses which required to schedule.
        course_count = self._count_of_select('kcYrs', '课程号', "不考试=0")
        # 非公选课门数=> 课程号!='00*'
        np_course_count = self._count_of_select('kcYrs', '课程号', "不考试=0 and 课程号 not like '00*'")
        # Todo: there's something wrong with kcYrs table schema(课程号 starts without 0), check and fix it later
        sql = "select 课程号 from kcYrs where 不考试=0 order by 选课人数 desc;"
        course_index = [r[0] for r in self.cursor.execute(sql).fetchall()]
        sql = "select 学号 from xsYkcm;"
        stu_index = [r[0] for r in self.cursor.execute(sql).fetchall()]

    def course_schedule(self):
        # premax是当前最大场次
        cur = self.conn.cursor()
        course_num = self._count_of_select('kcYrs', '课程号', "不考试=0")
        # 非公选课门数=> 课程号!='00*'
        student_num = self._count_of_select('学生与选课', '学号', "开课时间='{}'".format(self.exam_time))
        nonpub_course_num = self._count_of_select('kcYrs', '课程号', "不考试=0 and 课程号 not like '00*'")
        sql = "select 课程号,场次标识 from kcYrs where 不考试=0 order by 选课人数 desc;"
        # 处理预排数据，用于有听力或者已预先设定场次的考试，如卓老师在kcYrs表中设定的场次.
        # cos_idx_and_session [(course_number, index(场次标识), ()]
        course_idx_and_session = [r for r in self.cursor.execute(sql).fetchall()]
        course_index = [c[0] for c in course_idx_and_session]
        pre_session = [c[1] for c in course_idx_and_session]
        sql = "select 学号 from xsYkcm;"
        student_index = [r[0] for r in self.cursor.execute(sql).fetchall()]
        sql = "select 场次标识 from kcYrs order by 场次标识 desc ;"
        max_session = cur.execute(sql).fetchone()[0]
        pre_arranged_num = self._count_of_select('kcYrs', criteria='场次标识>0')
        # 把kcYrs表复制进数据
        # pre_arrange()
        # # 先排非公选课
        # non_pub_arrange()
        # create 2D array:course_num * student_num
        cs = {}
        # cs = [[0 for c in range(course_num)] for s in range(student_num)]
        sql = "select 课程号, 学号 from xsYxk;"
        result = [r for r in cur.execute(sql).fetchall()]
        for r in result:
            cs[r] = 1
            # try:
            #     cs[int(tmpa)][int(tmpb)] = 1
            # except Exception as e:
            #     logger.warning('Error while insert 2d array :CS[][],{},{}'.format(tmpa, tmpb))
        for key in cs:
            print(key, cs[key])

        loop = 0
        loop_cnt = 5  # 压缩次数
        for loop in range(loop_cnt):
            kcbs = max_session + 1
            done_session = pre_session
        # loop for all nonpub_course which haven't been arranged
        for i in range(nonpub_course_num - pre_arranged_num):
            from random import random
            end = (nonpub_course_num - pre_arranged_num - i + 1) * random(1) + 1
            begin = 0
            index = 1
            while begin < end:
                # Todo: following code won't work because course_idx in raw data are incorrect,check and fix it
                if done_session[index] == 0 and course_idx_and_session[index][:2] != '00':
                    begin += 1
                i += 1
            i -= 1

            for j in range(course_num):
                if done_session[j] != 0:
                    if self.merge_kc(course_index, cs, course_index[i], course_index[j]):
                        for k in range(course_num):
                            if k < j and done_session[k] == done_session[j]:
                                if self.merge_kc(course_index, cs, course_index[k], course_index[j]) = False:
                                    break

                        if k == course_num + 1:
                            done_session[i] = done_session[j]

            if j == course_num + 1:
                done_session[i] = kcbs
                kcbs += 1




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

    def _count_of_select(self, table, column='*', criteria=None):
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
        print(sql)
        cur.execute(sql)
        # cur.fetchall()[0]
        return cur.fetchone()[0]

    @staticmethod
    def merge_kc(course_index, cs, c1, c2):
        students = [key[1] for key in cs]
        for s in students:
            if cs((c1, s)) + cs((c2, s)) == 2:
                return False
        return True


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
