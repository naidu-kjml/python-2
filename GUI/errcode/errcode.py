from PyQt5.QtWidgets import QApplication, QWidget
import sys
from untitled import Ui_Form
import mysql.connector


class MyForm(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.search)  # 将按钮点击事件和search函数绑定

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    ui = MyForm(widget)
    widget.show()
    sys.exit(app.exec_())
