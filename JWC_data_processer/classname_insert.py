
import platform
import sqlite3


class class_insertor(object):
    def __init__(self):
        pass

    def db_init(db_path=None):
        """
        init db connection, Win&&Linux supported
        :return: conn
        """
        db_path = '219.229.250.19:1433'
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
            database = 'dbo'
            dsn = 'web'
            user = '090134'
            password = 'sadsad'
            # charset = 'GBK'
            # odbc_conn_str = "DRIVER={{SQL Server Native Client 11.0}};" \
            #                 "SERVER={};" \
            #                 "DATABASE={};" \
            #                 "UID={};" \
            #                 "PWD={};".format(db_path, database, user, password)
            odbc_conn_str = "DSN={};UID={};PWD={}".format(dsn, user, password)
            import pyodbc
            odbc_conn_str = odbc_conn_str
            print(odbc_conn_str)
            conn = pyodbc.connect(odbc_conn_str)
            return conn, conn.cursor()
        else:
            raise OSError('Unsupported OS')

    def get_course_info_by_t_id(self, cursor, t_id, split_class=True,
                                score_status=True):
        class_infos = []
        for i in range(1, 6):
            class_info = {}
            tmp_class_id = t_id + '#' + str(i)
            sql = "select * from dbo.班级 where 班级号='{}';".format(
                str(tmp_class_id))
            # Todo: test if execute result is null
            class_name = cursor.execute(sql).fetchone()
            # Todo: test if course_name already existed.
            if class_name:
                print('course_id already existed :{}'.format(class_name))
                continue
            else:
                sql_tea = "select 姓名 from 教工 where 教号={}".format(t_id)
                teacher_name = cursor.execute(sql_tea).fetchall()
                # class_name = "拆班教工" + teacher_name + "#" + i + "班"
                # sql = "select * from 班级 where 班级名称={}".format(class_name)
                if cursor.execute(sql).fetchone():
                    print(sql)
                    continue
                else:
                    class_info['class_id'] = tmp_class_id
                    class_info['class_name'] = class_name
                    if split_class:
                        class_info['class_prop'] = '02'
                    if score_status:
                        class_info['score_status'] = int(1)
            class_infos.append(class_info)
        return class_infos

    def insert_course_name(teacher_list):
        conn, cursor = class_insertor.db_init()
        for t_id in teacher_list:
            class_infos = class_insertor.get_course_info_by_t_id(cursor, t_id)
            for info in class_infos:
                sql = "insert into 班级 values ('{}','{}','{}',,,'{}',,,,,);".format(
                    info['class_id'], info['class_name'], info['class_prop'],
                    info['score_status'])
                print(sql)
                # Todo: cursor.execute(sql)


if __name__ == '__main__':
    teacher_list = ['090134']
    class_insertor.insert_course_name(teacher_list)
