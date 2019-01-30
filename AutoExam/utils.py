import subprocess
import sys


def testTable(tablename,cursor):
    if cursor.tables(table=tablename,tableType='TABLE').fetchone():
        return True
    else:
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
    mdb2sqlite(file,dest)

