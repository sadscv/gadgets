#!/usr/bin/env python
# -*- coding:utf-8 _*-
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

from tqdm import tqdm

DATABASE = sys.argv[1]


class Converter():
    def __init__(self, db):
        self.db = db

    def _table_names(self):
        # Get the list of table names with "mdb-tables"
        table_names = subprocess.Popen(["mdb-tables", "-1", self.db],
                                       stdout=subprocess.PIPE).communicate()[0]
        tables = table_names.splitlines()
        print("BEGIN")
        sys.stdout.flush()
        return tables

    def to_csv(self):
        """

        :return: list of filepath e.g. ~/AutoExam/data/2018-2019***.csv

        Dump each table in .mdb file to an CSV file
        """
        tables = self._table_names()
        files = []
        pbar = tqdm(tables)
        for t in pbar:
            if t != '':
                # convert " " in table names to "_" for the CSV filenames.
                contents = subprocess.Popen(["mdb-export", self.db,
                                             str(t, encoding='utf8').replace(" ", "_")],
                                            stdout=subprocess.PIPE).communicate()[0]
                if len(contents) != 0:
                    filename = str(t, encoding='utf8').replace(" ", "_") + str(".csv")
                    # Todo: make dir everytime instead of using /csv/, csv+currenttime.
                    file = open('./data/csv/' + filename, 'w+')
                    pbar.set_description('Dumping  {}'.format(filename))
                    # Dump each table as a CSV file using "mdb-export",
                    file.write(str(contents, encoding='utf8'))
                    files.append(os.path.abspath(file.name))
                    # files.append(file.name)
                    file.close()
                # files.append(os.getcwd() + str(filename))
            else:
                raise FileNotFoundError('{} is null'.format(t))
        # Todo:this may cause bugs.
        # Todo: add feature in _init_ func. clean the csv files.
        # should init or clean the csv file directory before use it
        print('Successful dump csv files:', files)
        return files

    def mdb2sqlite(self):

        # dump .mdb file to sqlite file
        files = self.to_csv()
        conn = sqlite3.connect(os.path.curdir + '/data/data.sqlite')
        # conn.set_trace_callback(print)
        # Todo: init or delete data.sqlite before execute following script
        conn.commit()

        pbar = tqdm(files)
        for file in pbar:
            sys.stdout.flush()
            pbar.set_description('Processing {}'.format(os.path.basename(file)))
            if file != '':
                # note: read_csv:head=None
                df = pandas.read_csv(file, delimiter='\t', error_bad_lines=False)
                f = os.path.basename(file).rstrip('.csv')
                df.to_sql(f, conn, if_exists='append', index=False,
                          index_label='ID')
        conn.close()
        sys.stdout.flush()


if __name__ == '__main__':
    conveter = Converter(sys.argv[1])
    conveter.mdb2sqlite()
