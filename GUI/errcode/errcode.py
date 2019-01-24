from PyQt5.QtWidgets import QApplication, QWidget
import sys
from untitled import Ui_Form
import mysql.connector


class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.response = ''

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
                    self.response = errcode + ':' + str(v[2]) + '\n' + self.response
                    self.textBrowser.setText(self.response)
                cursor.close()
            else:
                self.textBrowser.setText('错误码不存在')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyForm = MyForm()
    MyForm.show()
    sys.exit(app.exec_())
