# -*- coding: utf-8 -*-

import os


for file in os.listdir('.'):
    if file[-3: ] != 'xls':
        continue
    name = file.replace(' ', '')
    new_name = '开课拆班拟撤班_' + name
    os.rename(file, new_name)

