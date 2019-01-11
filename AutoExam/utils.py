def testTable(tablename,cursor):
    if cursor.tables(table=tablename,tableType='TABLE').fetchone():
        return True
    else:
        return False




