def testTable(tablename,cursor):
    if cursor.tables(table=tablename,tableType='TABLE').fetchone():
        return True
    else:
        return False


def delete_table(tablename, cursor):
    if testTable(tablename, cursor):
        cursor.execute("drop table {}".format(str(tablename)))
        print('deleting table:{}'.format(tablename))
        cursor.commit()


