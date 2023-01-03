from bs4 import BeautifulSoup
import requests
import re
import psycopg2
from SECCredentials import SEC_Credentials


def InsertIntoCrawlerInfo(cur,year,QTR,crawlerURL,crawlerID):
    cur.execute("insert into CrawlerInfo(year,QTR,crawlerURL,crawlerID) values(%s,%s,%s,%s);",
                (year,QTR,crawlerURL,crawlerID))
def CrawlerInfoScraping():
    conn = psycopg2.connect(host = SEC_Credentials.host,
                            port = SEC_Credentials.port,
                            user = SEC_Credentials.user,
                            password = SEC_Credentials.password,
                            database = "SECAnalysis")
    cur = conn.cursor()
    parentSECDirectoryUrl = "https://www.sec.gov/Archives/edgar/daily-index/"
    parentSECDirectoryContent = requests.get(parentSECDirectoryUrl)
    parentDirectorySoup = BeautifulSoup(parentSECDirectoryContent.content
                                    ,features="html.parser")
   
    for link in parentDirectorySoup.find_all('a'):
        YearSECDirectoryUrl = parentSECDirectoryUrl + link.get('href')
        yearMatch = re.search("20(1[6-9]|2[0-1])",YearSECDirectoryUrl )
        if yearMatch != None:
            fillingYear = yearMatch.group(0)
            YearSECDirectoryContent = requests.get(YearSECDirectoryUrl)
            YearSECDirectorySoup = BeautifulSoup(YearSECDirectoryContent.content,
                                                 features="html.parser")
            for qtrLink in YearSECDirectorySoup.find_all('a'):
                QTRSECDirectoryUrl = YearSECDirectoryUrl + qtrLink.get('href')
                qtrMatch = re.search("QTR[1-4]",QTRSECDirectoryUrl)
                if qtrMatch != None:
                    fillingQTR = qtrMatch.group(0)
                    QTRSECDirectoryContent = requests.get(QTRSECDirectoryUrl)
                    QTRSECDirectorySoup = BeautifulSoup(QTRSECDirectoryContent.content,
                                                        features="html.parser")
                    for fileLinks in QTRSECDirectorySoup.find_all('a'):
                        filematch = re.search("crawler",fileLinks.get('href'))
                        if filematch != None:
                            CrawlerFileFullPath = QTRSECDirectoryUrl + fileLinks.get('href')
                            print(fillingYear)
                            print(fillingQTR)
                            print(CrawlerFileFullPath)
                            print(str(len(CrawlerFileFullPath)))
                            print(fileLinks.get('href'))
                            InsertIntoCrawlerInfo(cur,int(fillingYear),int(fillingQTR[-1]),CrawlerFileFullPath,fileLinks.get('href'))
    conn.commit()
    cur.close()
    conn.close()
def ParseCrawlerFile(curr,CrawlerContents,crawlerUrl,crawlerID):
    CrawlerContents = bytes.decode(CrawlerContents.content,errors = "replace")
    
    
    barrierMatch = re.search("\-+\n",CrawlerContents)
    
    formList = CrawlerContents[barrierMatch.end():]
    formList = formList.split("\n")
    for entry in formList:
        filedDateMatch = re.search("20(1[0-9]|2[0-1])\d{4}",entry)
        try:
            if(filedDateMatch != None):

                filedDate = filedDateMatch.group(0)
                entry = re.sub(filedDate,'',entry)
                FormsUrlMatch = re.search("http\S*htm",entry)
                FormsUrl = FormsUrlMatch.group(0)
                entry = re.sub(FormsUrl,'',entry)
                entry = entry.strip()
                entry = re.split("\s{2,}",entry)
                CIK = entry[-1]
                FormType = entry[1]
                CompanyName = entry[0]
                print(FormsUrl)
                curr.execute("insert into formsubmissioninfo(CompanyName,crawlerUrl,crawlerID,CIK,DateSubmitted,FormUrl,FormType) values(%s,%s,%s,%s,%s,%s,%s)",
                             (CompanyName,crawlerUrl,crawlerID,CIK,filedDate,FormsUrl,FormType))
        except:
            print(entry)
            
def ReportGeneratingScraping():
    conn = psycopg2.connect(host = SEC_Credentials.host,
                            port = SEC_Credentials.port,
                            user = SEC_Credentials.user,
                            password = SEC_Credentials.password,
                            database = "SECAnalysis")
    curr = conn.cursor()
    curr.execute("SELECT crawlerURL,crawlerID FROM CrawlerInfo")

    crawlerinfo = curr.fetchall()
    curr.execute("SELECT crawlerURL,crawlerID from formsubmissioninfo where id=(SELECT max(id) from formsubmissioninfo)")
    if curr.rowcount > 0:
        checkpoint = curr.fetchone()
        LastStopped = crawlerinfo.index(checkpoint)
        crawlerinfo = crawlerinfo[LastStopped:]
        print(LastStopped)
    for urlId in crawlerinfo:
        crawlerurl = urlId[0]
        crawlerid = urlId[1]
        CrawlerUrlContent = requests.get(crawlerurl)
        ParseCrawlerFile(curr,CrawlerUrlContent,crawlerurl,crawlerid)
        conn.commit()
    curr.close()
    conn.close()
    return crawlerinfo

def insertIntoQuarter(curr,companyname,formurl,formtype,reporturl,formcontent):
    curr.execute("INSERT into quarter10(companyname,formurl,formtype,reporturl,formcontent) values (%s,%s,%s,%s,%s);",(companyname,formurl,formtype,reporturl,formcontent))
    
def QuarterFormScraping():
    conn = psycopg2.connect(host = SEC_Credentials.host,
                            port = SEC_Credentials.port,
                            user = SEC_Credentials.user,
                            password = SEC_Credentials.password,
                            database = "SECAnalysis")
    curr = conn.cursor()
    curr.execute("SELECT r.companyname,r.formtype,r.formurl FROM (SELECT * from formsubmissioninfo WHERE formtype = '10-Q' ) r left JOIN (SELECT companyname,formurl,formtype from quarter10) s ON (r.formurl,r.formtype) = (s.formurl,s.formtype) WHERE s.companyname is NULL")
    links = curr.fetchall()
    curr.execute("SELECT count(*) from quarter10")
    for link in links:
        formurl = link[-1]
        companyname = link[0]
        formtype = link[1]
        Request = requests.get(formurl)
        LinkSoup = BeautifulSoup(Request.content,features="html.parser")
        tables = LinkSoup.find_all('table')
        sizes = []
        for table in tables:
            rows = table.find_all("tr")

            cols = [tr for tr in rows if(tr.find(string='10-Q') != None)]
           
            if cols:
                Q10Doc = cols[0].find('a').get('href')
                Q10URL = "https://www.sec.gov"+Q10Doc
                curr.execute("SELECT * from quarter10 where companyname =%s AND formurl = %s AND formtype=%s AND reporturl=%s ",(companyname,formurl,formtype,Q10URL))
                       
                print(Q10URL)
                formcontent = requests.get(Q10URL).content
                insertIntoQuarter(curr,companyname,formurl,formtype,Q10URL,formcontent)
                conn.commit()
    curr.close()
    conn.close()

    
