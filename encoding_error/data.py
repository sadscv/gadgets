#coding=utf-8

import re, os, MySQLdb,urllib.request as req

######################## FileOperation脌脿拢潞掳眉潞卢露脭脦脛录镁碌脛虏脵脳梅拢篓脦陋脕脣卤茫脫脷碌梅脢脭潞脥鹿脹虏矛拢卢脦脪掳脩脥酶脪鲁脨脜脧垄脨麓脠毛脕脣脦脛录镁脰脨拢卢脣霉脪脭脫脨脕脣脮芒赂枚脦脛录镁虏脵脳梅脌脿拢漏##############################
class FileOperation():              
    
    def delFile(self, fileList):    # 脡戮鲁媒脦脛录镁
        for eachFile in fileList:
          if os.path.exists(eachFile):
            os.remove(eachFile)
        
    def writeToTxt(self, dataList, filePath): #陆芦脕脨卤铆脨麓脠毛脦脛录镁
        try:
            fp = open(filePath,"a")
            for item in dataList:
                fp.write(str(item))
            fp.close()
        except IOError:
            print("fail to open file")
            
######################## HtmlOperation脌脿拢潞掳眉潞卢露脭脥酶脪鲁碌脛虏脵脳梅################################################
class HtmlOperation():                
    
    def htmlRead(self, url):          # 露脕脠隆脥酶脪鲁
        try:
            htmlData = req.urlopen(url).read()
        except req.e:
                    print(req.e.reason)
        return htmlData
    
    def htmlRegex(self, strData, strRegex): # 赂霉戮脻脮媒脭貌卤铆麓茂脢陆拢卢麓脫脥酶脪鲁脰脨脤谩脠隆脢媒戮脻
        tags = re.findall(strRegex,strData,re.S)
        return tags
    
    def getRowData(self,data,regEx):      # 露脭脥酶脮戮脰脨卤铆赂帽脰脨碌脛脢媒戮脻陆酶脨脨麓娄脌铆拢卢碌脙碌陆鹿忙路露碌脛脢媒戮脻
        rowData = []
        allData = re.findall(regEx,data,re.S|re.M)
        for item in allData:    
            rowData.append(item.strip())
        return rowData
    
######################## ScoreDB脌脿拢潞掳眉潞卢露脭脢媒戮脻驴芒碌脛虏脵脳梅################################################
    
class ScoreDB():
    
    def __init__(self):             # 脕卢陆脫脢媒戮脻驴芒拢卢陆篓脕垄脫脦卤锚cursor
        self.conn = MySQLdb.connect(host='localhost', user='root',passwd='123456',charset='utf8')#麓脣麓娄脤铆录脫charset='utf8'脢脟脦陋脕脣脭脷脢媒戮脻驴芒脰脨脧脭脢戮脰脨脦脛拢卢麓脣卤脿脗毛卤脴脨毛脫毛脢媒戮脻驴芒碌脛卤脿脗毛脪禄脰脗
        self.cursor = self.conn.cursor()
        
    def createDB(self,dbName,tableCreateSQL):      # 麓麓陆篓脢媒戮脻驴芒
        self.cursor.execute('drop database if exists '+dbName) # 脧脠脡戮鲁媒脰庐脟掳碌脛脢媒戮脻驴芒拢卢脪脭脙芒脢媒戮脻脰脴赂麓
        self.cursor.execute('create database if not exists '+dbName) # 麓麓陆篓脢媒戮脻驴芒
        self.conn.select_db(dbName)              # 脩隆脭帽脢媒戮脻驴芒
        self.cursor.execute(tableCreateSQL)                        
        self.cursor.close()
        
    def commitDB(self,data):                        # 虏氓脠毛虏垄脤谩陆禄脢媒戮脻碌陆脢媒戮脻驴芒脰脨
        self.conn.select_db('scoredb')
        insertSql = "insert into scoregfkd(year,province,firstBatch,gcMax,gcMin,gcMean,xlMax,xlMin,xlMean) values (%s,'%s','%s','%s','%s','%s','%s','%s','%s')"% \
        (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
        self.cursor.execute(insertSql)
        self.conn.commit()
        self.cursor.close() 
    def showDB(self):
        self.conn.select_db('scoredb')
        self.cursor.execute("select * from scoregfkd")
        results = self.cursor.fetchall()
        for data in results:
            print(data[0],' ',data[1].decode("utf-8").encode("gbk"),' ',data[2],' ',data[3],' ',data[4],' ',data[5],' ',data[6],' ',data[7],' ',data[8])
        self.cursor.close()

######################## 脰梅潞炉脢媒 ################################################
    
if __name__=="__main__":

    fileOp = FileOperation()      # 脢碌脌媒禄炉脌脿
    htmlOp = HtmlOperation()    # 脢碌脌媒禄炉
    
    allCollegesUrl = "http://www.gxeduw.com/fsx/junxiao/" # 麓贸脩搂碌脛脥酶脰路

    # 脡戮鲁媒脰庐脟掳脡煤鲁脡碌脛脦脛录镁拢卢卤拢脰陇脙驴麓脦脡煤鲁脡碌脛脰脨录盲脦脛录镁脢脟脳卯脨脗碌脛隆拢
    fileOp.delFile(['allData.txt','gfkdUrl.txt','gfkdData.txt','scoreUrlList.txt','score3List.txt','eachYearData1.txt','eachYearData2.txt','eachYearData3.txt','tableList1.txt','tableList2.txt','tableList3.txt'])

    allData = htmlOp.htmlRead(allCollegesUrl)    
    fileOp.writeToTxt(allData,'allData.txt') # 麓忙脠隆脣霉脫脨戮眉脨拢路脰脢媒脧脽
    
    gfkdUrl = htmlOp.htmlRegex(allData,r'潞镁脛脧拢潞<a href="(.*?)">鹿煤路脌驴脝脩搂录录脢玫麓贸脩搂') # 禄帽脠隆鹿煤路脌驴脝麓贸碌脛路脰脢媒脧脽脥酶脰路
    fileOp.writeToTxt(gfkdUrl,'gfkdUrl.txt')  # 麓忙脠隆鹿煤路脌驴脝麓贸路脰脢媒脧脽Url
   
    gfkdUrlStr = gfkdUrl[0]
    gfkdData = htmlOp.htmlRead(gfkdUrlStr)
    fileOp.writeToTxt(gfkdData,'gfkdData.txt') # 露脕脠隆鹿煤路脌驴脝麓贸脌煤脛锚碌脛路脰脢媒脧脽脨脜脧垄
    
    scoreUrlList = htmlOp.htmlRegex(gfkdData,r'<dt><strong>鹿煤路脌驴脝脩搂录录脢玫麓贸脩搂路脰脢媒脧脽</strong>.*?鹿煤路脌驴脝脩搂录录脢玫麓贸脩搂2014脛锚赂梅脢隆脗录脠隆路脰脢媒脧脽</a></li>')
    fileOp.writeToTxt(scoreUrlList,'scoreUrlList.txt') 
    scoreUrlStr = scoreUrlList[0]
    score3List = htmlOp.htmlRegex(scoreUrlStr,r'<a href="(.*?)"  title=.*?</a></li>')
    fileOp.writeToTxt(score3List,'score3List.txt') # 脮脪碌陆3脛锚路脰脢媒碌脛脥酶脰路

    cnt=1
    yearList = [2016,2015,2014]       # 脛锚路脻碌脛脕脨卤铆拢卢脦陋脕脣脤铆录脫陆酶脢媒戮脻驴芒脳枚脳录卤赂
    allProvList = ['卤卤戮漏','脤矛陆貌','脡脧潞拢','脰脴脟矛','潞脫卤卤','潞脫脛脧','脭脝脛脧','脕脡脛镁','潞脷脕煤陆颅','潞镁脛脧','掳虏禄脮','脡陆露芦','脨脗陆庐','陆颅脣脮','脮茫陆颅','陆颅脦梅','潞镁卤卤','鹿茫脦梅','赂脢脣脿','脡陆脦梅','脛脷脙脡鹿脜','脡脗脦梅',
                 '录陋脕脰','赂拢陆篓','鹿贸脰脻','鹿茫露芦','脟脿潞拢','脦梅虏脴','脣脛麓篓','脛镁脧脛','潞拢脛脧','脤篓脥氓','脧茫赂脹','掳脛脙脜']

    dataList=[]
    for eachScoreUrl in score3List:  # 露脭脙驴赂枚脥酶脪鲁陆酶脨脨卤铆赂帽脢媒戮脻脤谩脠隆
        eachYearData = htmlOp.htmlRead(eachScoreUrl)
        fileOp.writeToTxt(eachYearData,'eachYearData'+str(cnt)+'.txt') # 碌脙碌陆麓贸卤铆赂帽

        if cnt == 1:
            tableList = htmlOp.htmlRegex(eachYearData,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # 碌脙碌陆脪禄赂枚赂枚脕脨卤铆脧卯
            
            for item in tableList:
                data = htmlOp.getRowData(item,r'nowrap="nowrap">(.*?)</td>')
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])   # 虏氓脠毛脛锚路脻脨脜脧垄
                    dataList.append(data)

        else:
            tableListMany = htmlOp.htmlRegex(eachYearData,r'<table>(.*?)</table>')  # 脫脡脫脷2014脛锚潞脥2015脛锚碌脛脥酶脪鲁陆谩鹿鹿潞脥2016脛锚碌脛虏禄脪禄脩霉拢卢脣霉脪脭虏禄脛脺脪禄脝冒麓娄脌铆隆拢脣霉脪脭脮芒脌茂脫脙脕脣if else
            tableList1=tableListMany[0]                                           # 2014,15脛锚碌脛脥酶脪鲁掳眉潞卢露脿赂枚table卤铆赂帽拢卢露酶脦脪脙脟脨猫脪陋碌脛脨脜脧垄脢脟碌脷脪禄赂枚卤铆赂帽拢卢脣霉脪脭脳枚麓脣麓娄脌铆
              
            tableList = htmlOp.htmlRegex(tableList1,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # 碌脙碌陆脪禄赂枚赂枚脕脨卤铆脧卯
            
            for item in tableList:
                data=htmlOp.getRowData(item.replace("x:str","000000000000"),r'<td 00000000000.*?>(.*?)</td>')  # 脥卢脩霉脪虏脢脟脪貌脦陋脥酶脪鲁陆谩鹿鹿拢卢脢媒戮脻陆谩鹿鹿碌脛脭颅脪貌拢卢脳枚鲁枚脮芒脩霉碌脛脤忙禄禄潞脥脮媒脭貌脝楼脜盲
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])  # 虏氓脠毛脛锚路脻脨脜脧垄
                    dataList.append(data)
        cnt = cnt+1
    for data in dataList:
        print(data[0],' ',data[1],' ',data[2],' ',data[3],' ',data[4],' ',data[5],' ',data[6],' ',data[7],' ',data[8])

    ScoreDB().createDB('scoredb','create table if not exists scoregfkd(year int,province varchar(100),firstBatch varchar(10),gcMax varchar(10),gcMin varchar(10),gcMean varchar(10),xlMax varchar(10),xlMin varchar(10),xlMean varchar(10))')        # 麓麓陆篓脢媒戮脻驴芒
    for data in dataList:       # 麓忙脠隆脢媒戮脻脠毛卤戮碌脴脢媒戮脻驴芒
        data[1] = data[1].decode("gbk").encode("utf-8")
        ScoreDB().commitDB(data)
    print('\nshow the database data:\n')
    ScoreDB().showDB()          # 脮鹿脢戮脢媒戮脻驴芒脰脨碌脛卤铆脢媒戮脻
