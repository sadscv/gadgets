# -*- coding: utf8 -*-

temp = '脌脿拢潞掳眉潞卢露脭脦脛录镁碌脛虏脵脳梅拢篓脦陋脕脣卤茫脫脷碌梅脢脭潞脥鹿脹虏矛拢卢脦脪掳脩脥酶脪鲁脨脜脧垄脨麓脠毛脕脣脦脛录镁脰脨拢卢脣霉脪脭脫脨脕脣脮芒赂枚脦脛录镁虏脵脳梅脌脿拢漏####'
# temp = '卤卤戮漏'
# file = temp.encode('utf8')
import chardet
# out = chardet.detect(file)
# print(out)
# t1 = temp.encode('utf8').decode('ISO-8859-1')
# f = open('tmp.txt', 'w')
# f.write('t1')
# f.close()
# f1 = open('tmp.txt', )
with open('./data.py', 'r') as f, open('./data_decode.py', 'w+') as fo:
    t1 = f.read().encode('gbk').decode('utf8').encode('latin-1').decode('gbk')
    fo.write(t1)
    print(t1)


# print(temp.encode('gbk').decode('utf8').encode('latin-1').decode('gbk'))
# for t in temp:
#     print(t.encode('utf8'))


# print(temp.encode('gbk').decode('utf8'))