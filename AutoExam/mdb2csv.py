#!/usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author: sadscv
@file: mdb2csv.py
@time: 2019/01/13 12:47
# Dump each table in an .mdb file to CSV files.
"""
import os
import sqlite3

import pandas
import subprocess
import sys

DATABASE = sys.argv[1]


def mdb2csv(tables, database):
    """

    :param tables:
    :param database:
    :return: list of filepath e.g. ~/AutoExam/data/2018-2019***.csv
    """
    files = []
    count = 0
    for t in tables:
        if t != '':
            # converting " " in table names to "_" for the CSV filenames.
            contents = subprocess.Popen(["mdb-export", database,
                                        str(t, encoding='utf8').replace(" ", "_")],
                                        stdout=subprocess.PIPE).communicate()[0]
            if len(contents) != 0:
                print('start', count)
                print(len(contents))
                print('\nend')
                count += 1
                filename = str(t, encoding='utf8').replace(" ", "_") + str(".csv")
                file = open('./data/csv/'+filename, 'w+')
                # print("Dumping " + filename)
                # Dump each table as a CSV file using "mdb-export",
                file.write(str(contents, encoding='utf8'))
                file.close()
                # files.append(file.name)
            files.append(filename)
        else:
            raise FileNotFoundError('{} is null'.format(t))
    # Todo:this may cause bugs.
    # should init or clean the csv file directory before use it
    return files


def mdb_converter(db, f_type='sqlite'):
    # schema = subprocess.Popen(["mdb-schema", db, "mysql"],
    #                           stdout=subprocess.PIPE).communicate()[0]
    # Get the list of table names with "mdb-tables"
    table_names = subprocess.Popen(["mdb-tables", "-1", db],
                                   stdout=subprocess.PIPE).communicate()[0]
    tables = table_names.splitlines()
    print("BEGIN")
    sys.stdout.flush()

    # Dump each table in .mdb file to an CSV file
    if f_type == 'csv':
        files = mdb2csv(tables, DATABASE)
        print('Successful dump csv files:')
        print(files)

    # dump .mdb file to sqlite file
    if f_type == 'sqlite':
        files = mdb2csv(tables, DATABASE)
        print(files)
        conn = sqlite3.connect(os.path.curdir + '/data/data.sqlite')
        # conn.set_trace_callback(print)
        cur = conn.cursor()
        # Todo: init or delete data.sqlite before execute following script
        cur.close()
        conn.commit()
        print(len(tables))
        for t in tables:
            pass
        for file in files:
            if file != '':
                # subprocess.call(["mdb-export", "-I", "mysql", DATABASE, file])
                #note: read_csv:head=None
                df = pandas.read_csv(os.path.join(os.path.curdir, 'data/csv/', file),
                                     delimiter='\t', error_bad_lines=False)
                # with pandas.option_context('display.max_colwidth', -1):
                #     print('$$$$$$')
                #     print(df.head(5))
                #     print('$$$$$$')
                df.to_sql(file.rstrip('.csv'), conn, if_exists='append', index=False, index_label='ID')
        print("COMMIT")
        conn.close()
        sys.stdout.flush()

############
# import csv, sqlite3
#
# cur.execute("CREATE TABLE t (col1, col2);") # use your column names here
#
# with open('data.csv','rb') as fin: # `with` statement available in 2.5+
#     # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['col1'], i['col2']) for i in dr]
#
# cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
# con.commit()
# con.close()
###########

if __name__ == '__main__':
    mdb_converter(DATABASE, f_type='sqlite')
