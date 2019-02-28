from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets, Qt
import sys, os, re, time
import requests
from untitled import Ui_Form
from selenium import webdriver


class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)

        self.thread = Worker()
        self.thread.sinOut.connect(self.slotAdd)


    def start(self):
        self.pushButton.setEnabled(False)
        self.thread.start()


    def slotAdd(self, file_inf):
        self.textBrowser.setText(file_inf)


class Worker(QThread):
    sinOut = pyqtSignal(str) # 自定义信号，执行run()函数时，从相关线程发射此信号

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        file_str = '程序启动中。。。'
        self.sinOut.emit(file_str)
        cookies = {
            'JSESSIONID': 'AA44EA56E2C53DA2733C9BC5B31CBE1C',
            'login': 'admin',
            'loginzh': 'undefined'
        }

        respon = requests.post('http://183.60.124.39:51181/tmis/dllAction!datagrid.action', cookies=cookies)

        a = respon.json()['rows']
        oa_list = []
        for i in a:
            oa_list.append(i['dll6'])

        respon = requests.post('http://183.60.124.39:51181/tmis/softAction!datagrid.action', cookies=cookies)
        a = respon.json()['rows']
        for i in a:
            try:
                oa_list.append(i['oanumber'])
            except:
                continue

        # 登录OA账号
        file_str = '正在登陆OA。。。'
        self.sinOut.emit(file_str)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=option)
        #browser = webdriver.Chrome()
        browser.implicitly_wait(5)
        browser.get("http://voa.grgbanking.com/")
        browser.find_element_by_id('UserName').clear()
        browser.find_element_by_id('UserName').send_keys('lyjie9')
        browser.find_element_by_id('UserKey').clear()
        browser.find_element_by_id('UserKey').send_keys('jrjk2100')
        browser.find_element_by_class_name('login_list_btn').click()
        time.sleep(3)
        try:
            browser.get('http://oa.grgbanking.com/vmobile/nav.php')
        except:
            file_str = '登陆失败'
            self.sinOut.emit(file_str)
            return

        file_str = '登陆成功！'
        self.sinOut.emit(file_str)
        # 切换到已办结页面
        browser.switch_to.frame('main')
        # time.sleep(1)
        browser.switch_to.frame('menu_top')
        # time.sleep(1)
        browser.find_element_by_xpath('//*[@id="navMenu"]/a[6]/span').click()
        # time.sleep(3)
        browser.switch_to.parent_frame()
        browser.switch_to.frame('menu_main')
        sum = 0
        for i in range(0, 50):
            # OA流程号
            oa = browser.find_element_by_xpath('//*[@id="%d"]/td[2]' % i).text
            if oa in oa_list:
                continue
            if browser.find_element_by_xpath('//*[@id="%d"]/td[3]/a' % i).text == "【运通智能】软件产品测试申请":
                browser.find_element_by_xpath('//*[@id="%d"]/td[4]/a' % i).click()
                # time.sleep(3)
                # 切换页面句柄
                handle = browser.current_window_handle
                while True:
                    time.sleep(1)
                    handles = browser.window_handles
                    if len(handles) == 2:
                        break
                for newhandle in handles:
                    if newhandle != handle:
                        browser.switch_to_window(newhandle)
                # time.sleep(1)
                browser.switch_to.frame('print_frm')
                # 类别
                try:
                    leibie = browser.find_element_by_xpath(
                        '//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[5]/td[3]/p').text.replace(u'\xa0', u' ')
                    m = re.match(r'【测试机型】\s?(.*?)\s?(?=【工控机】)', leibie.strip())
                    leibie = m.group(1).strip()
                except:
                    leibie = ''
                # 平台
                try:
                    pingtai = browser.find_element_by_xpath(
                        '//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[6]/td[2]/p').text.replace(u'\xa0', u' ')
                    m = re.match(r'【操作系统】\s?(.*?)\s?(?=【监控软件】)', pingtai.strip())
                    pingtai = m.group(1).strip()
                except:
                    pingtai = ''
                # 模块
                mokuai = browser.find_element_by_xpath(
                    '//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[2]/td[2]/div').text
                # 项目
                xiangmu = ''
                # 版本号
                banbenhao = browser.find_element_by_xpath(
                    '//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[3]/td[4]/div/p').text
                # 提交日期
                tjriqi = browser.find_element_by_xpath(
                    '//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[11]/td[2]/span/span/span').text
                m = re.match(r'(.*?)(\d+\-\d+\-\d+)\s.*?', tjriqi.strip())
                tjriqi = m.group(2).strip()
                # 提交人员
                tjry = m.group(1).strip()
                # 状态
                try:
                    if browser.find_element_by_xpath(
                            '//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[1]/td[2]/p[2]'):
                        zhuangtai = '测试完成'
                except:
                    zhuangtai = "配置管理完成"
                # 测试人员
                ceshirenyuan = browser.find_element_by_xpath(
                    '//*[@id="bodyScroll"]/form/div[2]/div/div/table/tbody/tr[3]/td[4]').text
                # 计划完成时间
                jhwcsj = browser.find_element_by_xpath(
                    '//*[@id="bodyScroll"]/form/div[2]/div/div/table/tbody/tr[3]/td[3]').text
                # 实际完成时间
                try:
                    sjwcsj = browser.find_element_by_xpath(
                        '//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[2]/td[2]/span[2]/p/span[2]/span').text
                    m = re.match(r'(.*?)(\d+\-\d+\-\d+)\s.*?', sjwcsj.strip())
                    sjwcsj = m.group(2).strip()
                except:
                    sjwcsj = ''
                # 测试结果
                try:
                    csjg = browser.find_element_by_xpath(
                        '//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[2]/td[2]/span[2]/p/span[1]').text
                except:
                    cejg = ''
                # 判断测试类型为驱动还是整机
                list = ['张昕', '周坤章', '陈丹鹏']
                if tjry in list:
                    postData = {
                        "version": leibie,
                        "dll1": pingtai,
                        "dll2": mokuai,
                        "dll3": '程序添加，需编辑！',
                        "dll4": banbenhao,
                        "dll5": tjriqi,
                        "dll6": oa,
                        "dll7": zhuangtai,
                        "dll8": ceshirenyuan,
                        "dll9": jhwcsj,
                        "dll10": sjwcsj,
                        "dll11": csjg,
                        "column20": '程序添加，需编辑！'
                    }

                    cookies = {
                        'JSESSIONID': 'AA44EA56E2C53DA2733C9BC5B31CBE1C',
                        'login': 'admin',
                        'loginzh': 'undefined'
                    }

                    try:
                        respon = requests.post('http://183.60.124.39:51181/tmis/dllAction!add.action', data=postData,
                                               cookies=cookies)
                        print('【%s】添加成功' % leibie)
                        file_str = '【%s】添加成功' % leibie
                        self.sinOut.emit(file_str)
                        sum += 1
                    except:
                        print('【%s】添加失败！！！' % leibie)
                else:
                    postData = {
                        'diqu': '程序添加，需编辑！',
                        'xianlu': xiangmu,
                        'sblx': mokuai,
                        'bbh': banbenhao,
                        'tjrq': tjriqi,
                        'oanumber': oa,
                        'status': zhuangtai,
                        'tester': ceshirenyuan,
                        'plantime': jhwcsj,
                        'nowtime': sjwcsj,
                        'testresult': csjg,
                        'column20': '程序添加，需编辑！'
                    }
                    cookies = {
                        'JSESSIONID': 'AA44EA56E2C53DA2733C9BC5B31CBE1C',
                        'login': 'admin',
                        'loginzh': 'undefined'
                    }
                    try:
                        respon = requests.post('http://183.60.124.39:51181/tmis/softAction!add.action', data=postData,
                                               cookies=cookies)
                        print('【%s】添加成功' % mokuai)
                        file_str = '【%s】添加成功' % mokuai
                        self.sinOut.emit(file_str)
                        sum += 1
                    except:
                        print('【%s】添加失败！！！' % mokuai)
                browser.close()
                browser.switch_to_window(handle)
                browser.switch_to.frame('main')
                browser.switch_to.frame('menu_main')
        browser.quit()
        print('程序结束，完成添加%d条记录' % sum)
        file_str = '程序结束，完成添加%d条记录' % sum
        self.sinOut.emit(file_str)


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(386, 127)
        MainWindow.setWindowIcon(QIcon('logo.png'))
        MainWindow.setStyleSheet("background-image:url(Background.jpg)")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 20, 100, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 50, 100, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(200, 24, 24, 12))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(200, 54, 24, 12))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tool by xjming"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入帐号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入密码"))
        self.label.setText(_translate("MainWindow", "帐号"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.pushButton.setText(_translate("MainWindow", "确定"))
        self.pushButton_2.setText(_translate("MainWindow", "取消"))

    def word_get(self):
        login_user = self.lineEdit.text()
        login_password = self.lineEdit_2.text()
        if login_user == 'lyjie9' and login_password == 'jrjk2100':
            MyForm.show()
            MainWindow.close()
        else:
            QMessageBox.warning(self,
                    "警告",
                    "用户名或密码错误！",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MyForm = MyForm()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())