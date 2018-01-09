#coding=utf-8

import re, os, MySQLdb,urllib.request as req

######################## FileOperation类：包含对文件的操作（为了便于调试和观察，我把网页信息写入了文件中，所以有了这个文件操作类）##############################
class FileOperation():              
    
    def delFile(self, fileList):    # 删除文件
        for eachFile in fileList:
          if os.path.exists(eachFile):
            os.remove(eachFile)
        
    def writeToTxt(self, dataList, filePath): #将列表写入文件
        try:
            fp = open(filePath,"a")
            for item in dataList:
                fp.write(str(item))
            fp.close()
        except IOError:
            print("fail to open file")
            
######################## HtmlOperation类：包含对网页的操作################################################
class HtmlOperation():                
    
    def htmlRead(self, url):          # 读取网页
        try:
            htmlData = req.urlopen(url).read()
        except req.e:
                    print(req.e.reason)
        return htmlData
    
    def htmlRegex(self, strData, strRegex): # 根据正则表达式，从网页中提取数据
        tags = re.findall(strRegex,strData,re.S)
        return tags
    
    def getRowData(self,data,regEx):      # 对网站中表格中的数据进行处理，得到规范的数据
        rowData = []
        allData = re.findall(regEx,data,re.S|re.M)
        for item in allData:    
            rowData.append(item.strip())
        return rowData
    
######################## ScoreDB类：包含对数据库的操作################################################
    
class ScoreDB():
    
    def __init__(self):             # 连接数据库，建立游标cursor
        self.conn = MySQLdb.connect(host='localhost', user='root',passwd='123456',charset='utf8')#此处添加charset='utf8'是为了在数据库中显示中文，此编码必须与数据库的编码一致
        self.cursor = self.conn.cursor()
        
    def createDB(self,dbName,tableCreateSQL):      # 创建数据库
        self.cursor.execute('drop database if exists '+dbName) # 先删除之前的数据库，以免数据重复
        self.cursor.execute('create database if not exists '+dbName) # 创建数据库
        self.conn.select_db(dbName)              # 选择数据库
        self.cursor.execute(tableCreateSQL)                        
        self.cursor.close()
        
    def commitDB(self,data):                        # 插入并提交数据到数据库中
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

######################## 主函数 ################################################
    
if __name__=="__main__":

    fileOp = FileOperation()      # 实例化类
    htmlOp = HtmlOperation()    # 实例化
    
    allCollegesUrl = "http://www.gxeduw.com/fsx/junxiao/" # 大学的网址

    # 删除之前生成的文件，保证每次生成的中间文件是最新的。
    fileOp.delFile(['allData.txt','gfkdUrl.txt','gfkdData.txt','scoreUrlList.txt','score3List.txt','eachYearData1.txt','eachYearData2.txt','eachYearData3.txt','tableList1.txt','tableList2.txt','tableList3.txt'])

    allData = htmlOp.htmlRead(allCollegesUrl)    
    fileOp.writeToTxt(allData,'allData.txt') # 存取所有军校分数线
    
    gfkdUrl = htmlOp.htmlRegex(allData,r'湖南：<a href="(.*?)">国防科学技术大学') # 获取国防科大的分数线网址
    fileOp.writeToTxt(gfkdUrl,'gfkdUrl.txt')  # 存取国防科大分数线Url
   
    gfkdUrlStr = gfkdUrl[0]
    gfkdData = htmlOp.htmlRead(gfkdUrlStr)
    fileOp.writeToTxt(gfkdData,'gfkdData.txt') # 读取国防科大历年的分数线信息
    
    scoreUrlList = htmlOp.htmlRegex(gfkdData,r'<dt><strong>国防科学技术大学分数线</strong>.*?国防科学技术大学2014年各省录取分数线</a></li>')
    fileOp.writeToTxt(scoreUrlList,'scoreUrlList.txt') 
    scoreUrlStr = scoreUrlList[0]
    score3List = htmlOp.htmlRegex(scoreUrlStr,r'<a href="(.*?)"  title=.*?</a></li>')
    fileOp.writeToTxt(score3List,'score3List.txt') # 找到3年分数的网址

    cnt=1
    yearList = [2016,2015,2014]       # 年份的列表，为了添加进数据库做准备
    allProvList = ['北京','天津','上海','重庆','河北','河南','云南','辽宁','黑龙江','湖南','安徽','山东','新疆','江苏','浙江','江西','湖北','广西','甘肃','山西','内蒙古','陕西',
                 '吉林','福建','贵州','广东','青海','西藏','四川','宁夏','海南','台湾','香港','澳门']

    dataList=[]
    for eachScoreUrl in score3List:  # 对每个网页进行表格数据提取
        eachYearData = htmlOp.htmlRead(eachScoreUrl)
        fileOp.writeToTxt(eachYearData,'eachYearData'+str(cnt)+'.txt') # 得到大表格

        if cnt == 1:
            tableList = htmlOp.htmlRegex(eachYearData,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # 得到一个个列表项
            
            for item in tableList:
                data = htmlOp.getRowData(item,r'nowrap="nowrap">(.*?)</td>')
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])   # 插入年份信息
                    dataList.append(data)

        else:
            tableListMany = htmlOp.htmlRegex(eachYearData,r'<table>(.*?)</table>')  # 由于2014年和2015年的网页结构和2016年的不一样，所以不能一起处理。所以这里用了if else
            tableList1=tableListMany[0]                                           # 2014,15年的网页包含多个table表格，而我们需要的信息是第一个表格，所以做此处理
              
            tableList = htmlOp.htmlRegex(tableList1,r'<tr>(.*?)</tr>')
            fileOp.writeToTxt(tableList,'tableList'+str(cnt)+'.txt')   # 得到一个个列表项
            
            for item in tableList:
                data=htmlOp.getRowData(item.replace("x:str","000000000000"),r'<td 00000000000.*?>(.*?)</td>')  # 同样也是因为网页结构，数据结构的原因，做出这样的替换和正则匹配
                if len(data)>0 and (data[0] in allProvList):
                    data.insert(0,yearList[cnt-1])  # 插入年份信息
                    dataList.append(data)
        cnt = cnt+1
    for data in dataList:
        print(data[0],' ',data[1],' ',data[2],' ',data[3],' ',data[4],' ',data[5],' ',data[6],' ',data[7],' ',data[8])

    ScoreDB().createDB('scoredb','create table if not exists scoregfkd(year int,province varchar(100),firstBatch varchar(10),gcMax varchar(10),gcMin varchar(10),gcMean varchar(10),xlMax varchar(10),xlMin varchar(10),xlMean varchar(10))')        # 创建数据库
    for data in dataList:       # 存取数据入本地数据库
        data[1] = data[1].decode("gbk").encode("utf-8")
        ScoreDB().commitDB(data)
    print('\nshow the database data:\n')
    ScoreDB().showDB()          # 展示数据库中的表数据
