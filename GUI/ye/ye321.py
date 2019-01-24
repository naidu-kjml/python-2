from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sys, os, re
from untitled import Ui_Form


class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        # 加载图片
        pic_list = self.piclist(r'D:\python\qsbk\img')
        self.label_1.setPixmap(QPixmap(pic_list[0]))
        self.label_2.setPixmap(QPixmap(pic_list[1]))
        self.label_3.setPixmap(QPixmap(pic_list[2]))
        self.label_4.setPixmap(QPixmap(pic_list[3]))
        self.label_5.setPixmap(QPixmap(pic_list[4]))
        self.label_6.setPixmap(QPixmap(pic_list[5]))
        self.label_7.setPixmap(QPixmap(pic_list[6]))
        self.label_8.setPixmap(QPixmap(pic_list[7]))
        self.label_9.setPixmap(QPixmap(pic_list[8]))
        self.label_10.setPixmap(QPixmap(pic_list[9]))
        self.label_11.setPixmap(QPixmap(pic_list[10]))
        self.label_12.setPixmap(QPixmap(pic_list[11]))
        self.label_13.setPixmap(QPixmap(pic_list[12]))
        self.label_14.setPixmap(QPixmap(pic_list[13]))
        self.label_15.setPixmap(QPixmap(pic_list[14]))
        self.label_16.setPixmap(QPixmap(pic_list[15]))
        self.label_17.setPixmap(QPixmap(pic_list[16]))
        self.label_18.setPixmap(QPixmap(pic_list[17]))
        self.label_19.setPixmap(QPixmap(pic_list[18]))
        self.label_20.setPixmap(QPixmap(pic_list[19]))
        self.label_21.setPixmap(QPixmap(pic_list[20]))
        self.label_22.setPixmap(QPixmap(pic_list[21]))
        self.label_23.setPixmap(QPixmap(pic_list[22]))
        self.label_24.setPixmap(QPixmap(pic_list[23]))
        self.label_25.setPixmap(QPixmap(pic_list[24]))
        self.label_26.setPixmap(QPixmap(pic_list[25]))
        self.label_27.setPixmap(QPixmap(pic_list[26]))
        self.label_28.setPixmap(QPixmap(pic_list[27]))
        self.label_29.setPixmap(QPixmap(pic_list[28]))
        self.label_30.setPixmap(QPixmap(pic_list[29]))
        self.label_31.setPixmap(QPixmap(pic_list[30]))
        self.label_32.setPixmap(QPixmap(pic_list[31]))
        self.label_1.setScaledContents(True)
        self.label_2.setScaledContents(True)
        self.label_3.setScaledContents(True)
        self.label_4.setScaledContents(True)
        self.label_5.setScaledContents(True)
        self.label_6.setScaledContents(True)
        self.label_7.setScaledContents(True)
        self.label_8.setScaledContents(True)
        self.label_9.setScaledContents(True)
        self.label_10.setScaledContents(True)
        self.label_11.setScaledContents(True)
        self.label_12.setScaledContents(True)
        self.label_13.setScaledContents(True)
        self.label_14.setScaledContents(True)
        self.label_15.setScaledContents(True)
        self.label_16.setScaledContents(True)
        self.label_17.setScaledContents(True)
        self.label_18.setScaledContents(True)
        self.label_19.setScaledContents(True)
        self.label_20.setScaledContents(True)
        self.label_21.setScaledContents(True)
        self.label_22.setScaledContents(True)
        self.label_23.setScaledContents(True)
        self.label_24.setScaledContents(True)
        self.label_25.setScaledContents(True)
        self.label_26.setScaledContents(True)
        self.label_27.setScaledContents(True)
        self.label_28.setScaledContents(True)
        self.label_29.setScaledContents(True)
        self.label_30.setScaledContents(True)
        self.label_31.setScaledContents(True)
        self.label_32.setScaledContents(True)

    def piclist(self, filepath):
        pic_list = []
        for i in os.listdir(filepath):
            pic_list.append(os.path.join(filepath, i))
        return pic_list

    def copy(self):
        r = re.match('复制链接(.*)', self.sender().text())
        index = int(r.group(1))
        self.lineEdit.setText(str(index))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyForm = MyForm()
    MyForm.show()
    sys.exit(app.exec_())

