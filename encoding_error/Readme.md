师弟提的一个编码问题把我难住了。仔细研究之后才了解这是个windows平台导致的错码错乱。被称作C2,C3问题
[参考链接 ](http://blog.zeerd.com/ffmpeg-c2c3-bug/)

Shell下
 
 `$cat file.py | iconv -f utf8 -t gbk | iconv -f utf8 -t latin1 | iconv -f gbk -t utf8`


这里是python[解决办法](https://gist.github.com/sadscv/80d4364a948cc54fadd23169bac5c311)