import platform
import pyodbc
import sqlite3


class course_insertor(object):

    def __init__(self):
        self.conn, self.cursor = self.db_init()

    def db_init(self, db_path=None):
        """
        init db connection, Win&&Linux supported
        :return: conn
        """
        db_path = '' # *.*.*.19:1433
        # db_path = config.dbpath
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
            user = ''
            password = ''
            odbc_conn_str = "DSN={};UID={};PWD={}".format(dsn, user, password)

            import pyodbc
            print(odbc_conn_str)
            conn = pyodbc.connect(odbc_conn_str)
            return conn, conn.cursor()
        else:
            raise OSError('Unsupported OS')

    def get_course_info_by_t_id(self, cursor, t_id, t_count, split_class=True,
                                score_status=True):
        """
        assign 5 class name to each teacher `t_id` at most. before we insert data
        we should test if the class_id and class_name have already existed in db.

        :param cursor:
        :param t_id:
        :param split_class:
        :param score_status:
        :return:
        """
        class_infos = []
        sql_tea = "select 姓名 from 教工 where 教号='{}';".format(t_id)
        teacher_name = cursor.execute(sql_tea).fetchone()[0]
        if not teacher_name:
            assert ValueError('no teacher_id existed on db'.format(t_id))
        # for i in range(1, 6):
        for i in range(1, t_count + 1):
            class_info = {}
            tmp_class_id = t_id + '#' + str(i)
            sql = "select * from dbo.班级 where 班级号='{}';".format(
                str(tmp_class_id))
            # Todo: test if execute result is null
            class_id = cursor.execute(sql).fetchone()
            # Todo: test if course_name already existed.
            if class_id:
                print('course_id already existed :{}'.format(class_id))
                continue
            else:
                class_name = "拆班教工" + teacher_name + "#" + str(i) + "班"
                sql = "select * from 班级 where 班级名称='{}';".format(class_name)
                print(sql)
                if cursor.execute(sql).fetchone():
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

    def insert_course_name(self, teacher_list):
        """

        :param teacher_list:
        :return:
        """
        self.conn_local, self.cursor_local = self.db_init_local()
        for t_id, t_count in teacher_list:
            class_infos = self.get_course_info_by_t_id(self.cursor, t_id,
                                                       t_count)
            for info in class_infos:
                sql = "INSERT into tmp_course " \
                      "VALUES ('{}','{}','{}',NULL,NULL,'{}',NULL,NULL,NULL,NULL,NULL);" \
                    .format(info['class_id'],
                            info['class_name'],
                            info['class_prop'],
                            info['score_status'])
                print('$', sql)
                # sql = "select * from tmp_tea_id"
                # while self.cursor_local.execute(sql).fetchall():
                #     try:
                #         result = self.cursor_local.fetchall()
                #         break
                #     except pyodbc.ProgrammingError:
                #         continue
                self.cursor_local.execute(sql).commit()
                # Todo: cursor.execute(sql)

    def db_init_local(self):
        db_path = "C:\\Users\sadscv\Desktop\外网.accdb"
        user = ''
        password = ''
        odbc_conn_str = "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" \
                        "DBQ=%s;" % (db_path)

        conn = pyodbc.connect(odbc_conn_str, autocommit=True)
        return conn, conn.cursor()

    def get_teacher_lists(self):
        conn_local, cursor_local = self.conn, self.cursor
        # sql = "select 教号, COUNT(教号) as 次数 from 音乐学院小课数据 group by 教号;"
        sql = "select 教号  from dbo.教工 where dbo.教工.教号 like 'jwc%';"
        result = cursor_local.execute(sql).fetchall()
        return result

    def insert_split_data(self, teacher_list):
        """

        :param teacher_list: [(t_id, num),()]
        :return:
        """

        conn_local, cursor_local = self.db_init_local()
        print(teacher_list)
        for t in teacher_list:
            sql = "select * from 音乐学院小课数据 where 教号='{}';".format(t[0])
            result = cursor_local.execute(sql).fetchall()
            tmp_tea_id = t[0]
            for i in range(t[1]):
                class_id = tmp_tea_id + '#' + str(i + 1)
                tmp = result[i][-1:][0]
                sql = "update 音乐学院小课数据 set 1='{}' where id={};".format(class_id,
                                                                       tmp)
                cursor_local.execute(sql)
                print(sql)
                cursor_local.commit()


if __name__ == '__main__':
    teacher_list = ['jwc046']
    insertor = course_insertor()
    teacher_list = insertor.get_teacher_lists()
    print(teacher_list)
    teacher_list = [(t[0].strip(), t[1]) for t in teacher_list]
    insertor.insert_course_name(teacher_list)
    # insertor.insert_split_data(teacher_list)
