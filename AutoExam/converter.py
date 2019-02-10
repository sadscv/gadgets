#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author: sadscv
@file: converter.py
@time: 2019/01/13 12:47
"""

import os
import sqlite3
import time
import pandas
import subprocess
import sys

from tqdm import tqdm

DATABASE = sys.argv[1]


class Converter:
    def __init__(self, mdb):
        self.mdb = mdb
        self.conn = self.db_init()

    def db_init(self):
        """
        create sqlite db with given schema on .mdb file
        :return: conn
        """
        schema = subprocess.Popen(["mdb-schema", self.mdb, "mysql"],
                                  stdout=subprocess.PIPE).communicate()[0]
        conn = sqlite3.connect(os.path.curdir + '/data/{}[{}].sqlite'.
                               format(os.path.basename(self.mdb).rsplit('.')[0], time.strftime("%H:%M")))
        # conn.set_trace_callback(print)
        cur = conn.cursor()
        cur.executescript(str(schema, encoding='utf8'))
        cur.close()
        conn.commit()
        return conn

    def _table_names(self):
        # Get the list of table names with "mdb-tables"
        table_names = subprocess.Popen(["mdb-tables", "-1", self.mdb],
                                       stdout=subprocess.PIPE).communicate()[0]
        tables = table_names.splitlines()
        print("BEGIN")
        sys.stdout.flush()
        return tables

    def to_csv(self):
        """
        Dump each table in .mdb file to  CSV file
        :return: list of filepath  e.g. [~/data/2018-2019***.csv, ~/....]
        """
        tables = self._table_names()
        files = []
        pbar = tqdm(tables)
        for t in pbar:
            if t != '':
                # Dump each table as a CSV file using "mdb-export",
                contents = subprocess.Popen(["mdb-export", self.mdb,
                                            str(t, encoding='utf8').replace(" ", "_")],
                                            stdout=subprocess.PIPE).communicate()[0]
                if len(contents) != 0:
                    filename = str(t, encoding='utf8').replace(" ", "_") + str(".csv")
                    file = open('./data/csv/' + filename, 'w+')
                    pbar.set_description('Dumping  {}'.format(filename))
                    file.write(str(contents, encoding='utf8'))
                    files.append(os.path.abspath(file.name))
                    file.close()
            else:
                raise FileNotFoundError('{} is null'.format(t))
        print('Successfully dump csv files:', files)
        return files

    def mdb2sqlite(self):
        """
        dump .mdb file to sqlite file
        :return: None
        """
        files = self.to_csv()
        pbar = tqdm(files)
        for file in pbar:
            sys.stdout.flush()
            pbar.set_description('Processing {}'.format(os.path.basename(file)))
            if file != '':
                # note: read_csv:head=None
                df = pandas.read_csv(file, header=0, error_bad_lines=False, delimiter=',')
                f = os.path.basename(file).rstrip('.csv')
                df.to_sql(f, self.conn, if_exists='append', index=False,
                          index_label='ID')
        self.conn.close()
        sys.stdout.flush()


if __name__ == '__main__':
    converter = Converter(sys.argv[1])
    converter.mdb2sqlite()
