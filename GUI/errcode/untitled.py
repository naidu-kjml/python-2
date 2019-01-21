# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(300, 30, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.search)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 31))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(20, 90, 361, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(80, 30, 201, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "模块错误码查询"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.label.setText(_translate("Form", "错误码："))

    def search(self):
        errcode = self.lineEdit.text()
        if errcode == '':
            self.textBrowser.setText('错误码为空')
        else:
            conn = mysql.connector.connect(user='root', password='123456', database='errcode')
            cursor = conn.cursor()
            cursor.execute('select * from errcode where errcode =%s', (errcode,))
            values = cursor.fetchall()
            if values:
                for v in values:
                    self.textBrowser.setText(str(v[2]))
                cursor.close()
            else:
                self.textBrowser.setText('错误码不存在')


if __name__=="__main__":
    import sys
    from PyQt5.QtGui import QIcon
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QWidget()
    ui=Ui_Form()
    ui.setupUi(widget)
    widget.setWindowIcon(QIcon('web.ico'))#增加icon图标，如果没有图片可以没有这句
    widget.show()
    sys.exit(app.exec_())
