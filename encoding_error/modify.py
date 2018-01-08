# -*- coding: cp936 -*-

temp = '### FileOperationÀà£º°üº¬¶ÔÎÄ¼þµÄ²Ù×÷£¨ÎªÁË±ãÓÚµ÷ÊÔºÍ¹Û²ì£¬ÎÒ°ÑÍøÒ³ÐÅÏ¢Ð´ÈëÁËÎÄ¼þÖÐ£¬ËùÒÔÓÐÁËÕâ¸öÎÄ¼þ²Ù×÷Àà£©####'
# temp = '±±¾©'
# file = temp.encode('utf8')
import chardet
# out = chardet.detect(file)
# print(out)
# t1 = temp.encode('utf8').decode('ISO-8859-1')
# f = open('tmp.txt', 'w')
# f.write('t1')
# f.close()
# f1 = open('tmp.txt', )
origin = open('./data.py', 'rb')

t2 = origin.read().decode('utf-8').encode('ISO-8859-1').decode('utf-8')
# print(temp.encode('utf8').decode('ISO-8859-1'))
# for t in temp:
#     print(t.encode('utf8'))


# print(temp.encode('gbk').decode('utf8'))