#encoding=utf-8
'''
Created on 2016年7月22日
@author: Mr.Bubbles
'''

import urllib,urllib2,re,cookielib
from urllib2 import URLError

class CORE:
    def __init__(self,username,password):
        self.login_url='http://222.195.8.201/pass.asp'
        self.grade_url='http://222.195.8.201/student/asp/Select_Success.asp'
        self.curriculum_url='http://222.195.8.201/student/asp/grkb2.asp'
        self.myinfo_url='http://222.195.8.201/student/asp/xsxxxxx.asp'
        self.filename='cookie.txt'
        self.gradeList=[]
        self.username=username
        self.password=password
    #获取一页的所有代码
    def getPage(self):
        #file=open('C:\\Users\\Mr.Bubbles\\Desktop\\test.html','w')
        cookie=cookielib.MozillaCookieJar(self.filename)
        handler=urllib2.HTTPCookieProcessor(cookie)
        opener=urllib2.build_opener(handler)
        values={'UserStyle':'student',
                'user':self.username,
                'password':self.password}
        data=urllib.urlencode(values)   #对于post数据进行编码
        opener.open(self.login_url,data) #模拟登录
        cookie.save(self.filename, ignore_discard=True, ignore_expires=True)
        response=opener.open(self.grade_url)
        html=response.read().decode("gb2312")       #统一强制转换为Unicode
        #file.write(html.encode('gb2312'))
        return html
    #模式匹配获取成绩存入列表
    def getGrade(self):
        try:
            html=self.getPage()
            #print html
            #构建匹配字符串
            name_str='<tr.*?bgcolor=.*?>.*?<td>(.*?)</td>.*?<td.*?align.*?>(.*?)</td>.*?<td>(.*?)</td>'
            grade_str='.*?<td.*?align.*?>.*?</td>.*?<td.*?align.*?>(.*?)</td>'
            score_str='.*?<td.*?align.*?>.*?</td>.*?<td>(.*?)</td>'
            special_pattern=re.compile('<.*?>')
            #进行匹配
            pattern_str=name_str+grade_str+score_str
            pattern=re.compile(pattern_str,re.S|re.I)
            items=re.findall(pattern,html)
            if items:
                for item in items:
                    newitem=re.sub(special_pattern,'',item[3])   #特殊成绩的格式过滤
                    isenglish=item[2].find(u'英语')
                    self.gradeList.append([item[0],item[1],item[2],newitem,item[4],isenglish])
                    
                    #print item[0].strip(),' ',item[1].strip(),'   ',item[2].strip(),'   ',item[3].strip(),' ',item[4].strip() #for debug
                return True
            else:
                return None
        except URLError:
            print 'Invalid username or password!'
    def calcGPA(self):
        if self.getGrade()==None:
            return None
        else:
            totalCredit=0   #绩点学分乘积和
            sum=0           #学分和
            enUpFlag=0      #英语免修修正
            #遍历整个成绩单并且根据规则计算GPA
            for item in self.gradeList[::-1]: #逆序遍历
                weight=1                    #乘积和的系数
                singleGPA=0                 #单门课程的GPA
                cDate=item[0].strip()
                cCode=item[1].strip()
                cName=item[2].strip()
                cGrade=item[3].strip()
                cCredit=item[4].strip()
                cIsEnglish=item[5]
                if cGrade.isdigit():
                    cGrade=int(cGrade)
                    if cGrade<60:
                        singleGPA=0
                    elif cGrade>=60 and cGrade<64:
                        singleGPA=1.0
                    elif cGrade>=64 and cGrade<66:
                        singleGPA=1.3
                    elif cGrade>=66 and cGrade<68:
                        singleGPA=1.7
                    elif cGrade>=68 and cGrade<72:
                        singleGPA=2.0
                    elif cGrade>=72 and cGrade<75:
                        singleGPA=2.3
                    elif cGrade>=75 and cGrade<78:
                        singleGPA=2.7
                    elif cGrade>=78 and cGrade<82:
                        singleGPA=3.0
                    elif cGrade>=82 and cGrade<85:
                        singleGPA=3.3
                    elif cGrade>=85 and cGrade<90:
                        singleGPA=3.7
                    elif cGrade>=90 and cGrade<95:
                        singleGPA=4.0
                    elif cGrade>=95 and cGrade<=100:
                        singleGPA=4.3
                else:
                    if cGrade==u'免修':         #前提是英语课程才会出现免修
                        enUpFlag=1
                    elif cGrade==u'优':
                        singleGPA=3.9
                    elif cGrade==u'良':
                        singleGPA=3.0
                    elif cGrade==u'中':
                        singleGPA=2.0
                    elif cGrade==u'及格':
                        singleGPA=1.2
                    elif cGrade==u'不及格':
                        singleGPA=0
                if cIsEnglish!=-1 and enUpFlag==1:      #对于免修英语的不同处理过程
                    weight=1.1
                else:
                    weight=1
                totalCredit+=weight*singleGPA*float(cCredit)
                sum+=float(cCredit)
                #print cDate,cCode,cName,cGrade,cCredit
            GPA=totalCredit/sum 
            return GPA  
#core=CORE('2013217142','225541')        #for debug
#print core.calcGPA()