# -*- coding: cp936 -*-
#coding=utf-8
import re, os, MySQLdb,urllib.request as req

######################## FileOperationÀà£º°üº¬¶ÔÎÄ¼þµÄ²Ù×÷£¨ÎªÁË±ãÓÚµ÷ÊÔºÍ¹Û²ì£¬ÎÒ°ÑÍøÒ³ÐÅÏ¢Ð´ÈëÁËÎÄ¼þÖÐ£¬ËùÒÔÓÐÁËÕâ¸öÎÄ¼þ²Ù×÷Àà£©##############################
class FileOperation():              
    
    def delFile(self, fileList):    # É¾³ýÎÄ¼þ
        for eachFile in fileList:
          if os.path.exists(eachFile):
            os.remove(eachFile)
        
    def writeToTxt(self, dataList, filePath): #½«ÁÐ±íÐ´ÈëÎÄ¼þ
        try:
            fp = open(filePath,"a")
            for item in dataList:
                fp.write(str(item))
            fp.close()
        except IOError:
            print("fail to open file")
            
######################## HtmlOperationÀà£º°üº¬¶ÔÍøÒ³µÄ²Ù×÷################################################
class HtmlOperation():                
    
    def htmlRead(self, url):          # ¶ÁÈ¡ÍøÒ³
        try:
            htmlData = req.urlopen(url).read()
        except req.e:
                    print(req.e.reason)
        return htmlData
    
    def htmlRegex(self, strData, strRegex): # ¸ù¾ÝÕýÔò±í´ïÊ½£¬´ÓÍøÒ³ÖÐÌáÈ¡Êý¾Ý
        tags = re.findall(strRegex,strData,re.S)
        return tags
    
    def getRowData(self,data,regEx):      # ¶ÔÍøÕ¾ÖÐ±í¸ñÖÐµÄÊý¾Ý½øÐÐ´¦Àí£¬µÃµ½¹æ·¶µÄÊý¾Ý
        rowData = []
        allData = re.findall(regEx,data,re.S|re.M)
        for item in allData:    
            rowData.append(item.strip())
        return rowData
    
######################## ScoreDBÀà£º°üº¬¶ÔÊý¾Ý¿âµÄ²Ù×÷################################################
    
class ScoreDB():
    
    def __init__(self):             # Á¬½ÓÊý¾Ý¿â£¬½¨Á¢ÓÎ±êcursor
        self.conn = MySQLdb.connect(host='localhost', user='root',passwd='123456',charset='utf8')#´Ë´¦Ìí¼Ócharset='utf8'ÊÇÎªÁËÔÚÊý¾Ý¿âÖÐÏÔÊ¾ÖÐÎÄ£¬´Ë±àÂë±ØÐëÓëÊý¾Ý¿âµÄ±àÂëÒ»ÖÂ
        self.cursor = self.conn.cursor()
        
    def createDB(self,dbName,tableCreateSQL):      # ´´½¨Êý¾Ý¿â
        self.cursor.execute('drop database if exists '+dbName) # ÏÈÉ¾³ýÖ®Ç°µÄÊý¾Ý¿â£¬ÒÔÃâÊý¾ÝÖØ¸´
        self.cursor.execute('create database if not exists '+dbName) # ´´½¨Êý¾Ý¿â
        self.conn.select_db(dbName)              # Ñ¡ÔñÊý¾Ý¿â
        self.cursor.execute(tableCreateSQL)                        
        self.cursor.close()
        
    def commitDB(self,data):                        # ²åÈë²¢Ìá½»Êý¾Ýµ½Êý¾Ý¿âÖÐ
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

######################## Ö÷º¯Êý ################################################
    
if __name__=="__main__":

    fileOp = FileOperation()      # ÊµÀý»¯Àà
    htmlOp = HtmlOperation()    # ÊµÀý»¯
    
    allCollegesUrl = "http://www.gxeduw.com/fsx/junxiao/" # ´óÑ§µÄÍøÖ·

    # É¾³ýÖ®Ç°Éú³ÉµÄÎÄ¼þ£¬±£Ö¤Ã¿´ÎÉú³ÉµÄÖÐ¼äÎÄ¼þÊÇ×îÐÂµÄ¡£
    fileOp.delFile(['allData.txt','gfkdUrl.txt','gfkdData.txt','scoreUrlList.txt','score3List.txt','eachYearData1.txt','eachYearData2.txt','eachYearData3.txt','tableList1.txt','tableList2.txt','tableList3.txt'])

    allData = htmlOp.htmlRead(allCollegesUrl)    
    fileOp.writeToTxt(allData,'allData.txt') # ´æÈ¡ËùÓÐ¾üÐ£·ÖÊýÏß
    
    gfkdUrl = htmlOp.htmlRegex(allData,r'ºþÄÏ£º<a href="(.*?)">¹ú·À¿ÆÑ§¼¼Êõ´óÑ§') # »ñÈ¡¹ú·À¿Æ´óµÄ·ÖÊýÏßÍøÖ·
    fileOp.writeToTxt(gfkdUrl,'gfkdUrl.txt')  # ´æÈ¡¹ú·À¿Æ´ó·ÖÊýÏßUrl
   
    gfkdUrlStr = gfkdUrl[0]
    gfkdData = htmlOp.htmlRead(gfkdUrlStr)
    fileOp.writeToTxt(gfkdData,'gfkdData.txt') # ¶ÁÈ¡¹ú·À¿Æ´óÀúÄêµÄ·ÖÊýÏßÐÅÏ¢
    
    scoreUrlList = htmlOp.htmlRegex(gfkdData,r'<dt><strong>¹ú·À¿ÆÑ§¼¼Êõ´óÑ§·ÖÊýÏß</strong>.*?¹ú·À¿ÆÑ§¼¼Êõ´óÑ§2014Äê¸÷Ê¡Â¼È¡·ÖÊýÏß</a></li>')
    fileOp.writeToTxt(scoreUrlList,'scoreUrlList.txt') 
    scoreUrlStr = scoreUrlList[0]
    score3List = htmlOp.htmlRegex(scoreUrlStr,r'<a href="(.*?)"  title=.*?</a></li>')
    fileOp.writeToTxt(score3List,'score3List.txt') # ÕÒµ½3Äê·ÖÊýµÄÍøÖ·

    cnt=1
    yearList = [2016,2015,2014]       # Äê·ÝµÄÁÐ±í£¬ÎªÁËÌí¼Ó½øÊý¾Ý¿â×ö×¼±¸
    allProvList = ['±±¾©','Ìì½ò','ÉÏº£','ÖØÇì','ºÓ±±','ºÓÄÏ','ÔÆÄÏ','ÁÉÄþ','ºÚÁú½­','ºþÄÏ','°²»Õ','É½¶«','ÐÂ½®','½­ËÕ','Õã½­','½­Î÷','ºþ±±','¹ãÎ÷','¸ÊËà','É½Î÷','ÄÚÃÉ¹Å','ÉÂÎ÷',
                 '¼ªÁÖ','¸£½¨','¹óÖÝ','¹ã¶«','Çàº£','Î÷²Ø','ËÄ´¨','ÄþÏÄ','º£ÄÏ','Ì¨Íå','Ïã¸Û','°ÄÃÅ']

    dataList=[]
    for eachScoreUrl in score3List:  # ¶ÔÃ¿¸öÍøÒ³½øÐÐ±í¸ñÊý¾ÝÌáÈ¡
        eachYearData = htmlOp.htmlRead(eachScoreUrl)
        fileOp.writeToTxt(eachYearData,'eachYearData'+str(cnt)+'.txt') # µÃµ½´ó±í¸ñ

        if cnt == 1:
            tableList = htmlOp.htmlRegex(eachYearData,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # µÃµ½Ò»¸ö¸öÁÐ±íÏî
            
            for item in tableList:
                data = htmlOp.getRowData(item,r'nowrap="nowrap">(.*?)</td>')
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])   # ²åÈëÄê·ÝÐÅÏ¢
                    dataList.append(data)

        else:
            tableListMany = htmlOp.htmlRegex(eachYearData,r'<table>(.*?)</table>')  # ÓÉÓÚ2014ÄêºÍ2015ÄêµÄÍøÒ³½á¹¹ºÍ2016ÄêµÄ²»Ò»Ñù£¬ËùÒÔ²»ÄÜÒ»Æð´¦Àí¡£ËùÒÔÕâÀïÓÃÁËif else
            tableList1=tableListMany[0]                                           # 2014,15ÄêµÄÍøÒ³°üº¬¶à¸ötable±í¸ñ£¬¶øÎÒÃÇÐèÒªµÄÐÅÏ¢ÊÇµÚÒ»¸ö±í¸ñ£¬ËùÒÔ×ö´Ë´¦Àí
              
            tableList = htmlOp.htmlRegex(tableList1,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # µÃµ½Ò»¸ö¸öÁÐ±íÏî
            
            for item in tableList:
                data=htmlOp.getRowData(item.replace("x:str","000000000000"),r'<td 00000000000.*?>(.*?)</td>')  # Í¬ÑùÒ²ÊÇÒòÎªÍøÒ³½á¹¹£¬Êý¾Ý½á¹¹µÄÔ­Òò£¬×ö³öÕâÑùµÄÌæ»»ºÍÕýÔòÆ¥Åä
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])  # ²åÈëÄê·ÝÐÅÏ¢
                    dataList.append(data)
        cnt = cnt+1
    for data in dataList:
        print(data[0],' ',data[1],' ',data[2],' ',data[3],' ',data[4],' ',data[5],' ',data[6],' ',data[7],' ',data[8])

    ScoreDB().createDB('scoredb','create table if not exists scoregfkd(year int,province varchar(100),firstBatch varchar(10),gcMax varchar(10),gcMin varchar(10),gcMean varchar(10),xlMax varchar(10),xlMin varchar(10),xlMean varchar(10))')        # ´´½¨Êý¾Ý¿â
    for data in dataList:       # ´æÈ¡Êý¾ÝÈë±¾µØÊý¾Ý¿â
        data[1] = data[1].decode("gbk").encode("utf-8")
        ScoreDB().commitDB(data)
    print('\nshow the database data:\n')
    ScoreDB().showDB()          # Õ¹Ê¾Êý¾Ý¿âÖÐµÄ±íÊý¾Ý
