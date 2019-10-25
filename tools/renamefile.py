# -*- coding: utf-8 -*-

import os


for file in os.listdir('.'):
    if file[-3: ] != 'xls':
        continue
    name = file.replace(' ', '')
    new_name = '1-6-2在职教师-' + name
    # new_name = name[:-9]
    os.rename(file, new_name)

