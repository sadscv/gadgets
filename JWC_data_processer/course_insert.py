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

    def insert_ChaiBan(self, course_num, class_nums, teacher_list,
                       classroom_list):
        """

        :param teacher_list:
        :return:
        """
        tmp_cls_list = []
        for i in range(5):
            for c in classroom_list:
                tmp_cls_list.append(c)
        classroom_list = tmp_cls_list
        self.conn_local, self.cursor_local = self.db_init_local()
        for i in range(len(class_nums)):
            sql = "INSERT into tmp_courses " \
                  "VALUES ('{}','{}','{}','{}','{}','Z','60','60','60','60',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{}','2019/7/1 02:14:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL,NULL);" \
                .format('2019-9-1',
                        course_num,
                        class_nums[i],
                        class_nums[i],
                        teacher_list[i],
                        classroom_list[i]
                        )
            self.cursor_local.execute(sql)
            # sql = "select * from tmp_tea_id"
            # while self.cursor_local.execute(sql).fetchall():
            #     try:
            #         result = self.cursor_local.fetchall()
            #         break
            #     except pyodbc.ProgrammingError:
            #         continue
            # self.cursor_local.execute(sql).commit()
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
        sql = "select 教号  from dbo.教工 where dbo.教工.教号 like '00待定%';"
        result = cursor_local.execute(sql).fetchall()
        clean = []
        for i in range(3):
            for row in result:
                for i in row:
                    clean.append(i)
        return clean

    def get_classroom_list(self):
        conn_local, cursor_local = self.conn, self.cursor
        # sql = "select 教号, COUNT(教号) as 次数 from 音乐学院小课数据 group by 教号;"
        sql = "select 教室号  from dbo.教室 where dbo.教室.教室号 like 'V%';"
        result = cursor_local.execute(sql).fetchall()
        clean = []
        for i in range(2):
            for row in result:
                for i in row:
                    clean.append(i)
        return clean

    def insert_split_data(self, teacher_list):
        """

        :param teacher_list: [(t_id, num),()]
        :return:
        """
        conn_local, cursor_local = self.db_init_local()
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

    def get_class_num(self, course_num):
        sql = "select 班级号 from dbo.开课计划 where 课程号='{}' and 开课时间='2019-9-1'".format(
            course_num)
        result = self.cursor.execute(sql).fetchall()
        clean = []
        for row in result:
            for i in row:
                clean.append(i)
        return clean


if __name__ == '__main__':
    insertor = course_insertor()
    teacher_list = insertor.get_teacher_lists()
    # teacher_list = [(t[0].strip(), t[1]) for t in teacher_list]
    course_num = '056001'
    class_nums = insertor.get_class_num(course_num)
    classroom_list = insertor.get_classroom_list()
    print(class_nums)
    # insertor.insert_ChaiBan(course_num, class_nums,
    #                         teacher_list,classroom_list)
    # insertor.insert_AnPai(course_num, class_nums, teacher_list, )
    # insertor.insert_split_data(teacher_list)
