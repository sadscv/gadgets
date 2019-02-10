import subprocess
import sys


def testTable(tablename, cursor, platform='Windows'):
    if platform == 'Linux':
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
        if cursor.execute(sql):
            return True
    else:
        if cursor.tables(table=tablename, tableType='TABLE').fetchone():
            return True
        return False


def mdb2sqlite(file, dest):
    subprocess.call(["mdb-schema", file, "mysql"])
    table_names = subprocess.Popen(["mdb-tables", "-1", file],
                                   stdout=subprocess.PIPE).communicate()[0]
    sys.stdout.flush()


def delete_table(tablename, cursor):
    if testTable(tablename, cursor):
        cursor.execute("drop table {}".format(str(tablename)))
        print('deleting table:{}'.format(tablename))
        cursor.commit()


if __name__ == '__main__':
    mdb2sqlite(file, dest)
