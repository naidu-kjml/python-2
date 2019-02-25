from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sys, os, re, time
from untitled import Ui_Form
from ye import Ye


class MyForm(QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.links = []
        if not os.path.exists(r'D:\python\GUI\ye\1'):
            os.mkdir(r'D:\python\GUI\ye\1')
        try:
            with open(r'D:\python\GUI\ye\1\link.txt', 'r') as f:
                self.links = f.readlines()
        except:
            pass
        # 加载图片
        try:
            self.label_1.setPixmap(QPixmap(r'D:\python\GUI\ye\1\1.jpg'))
            self.label_2.setPixmap(QPixmap(r'D:\python\GUI\ye\1\2.jpg'))
            self.label_3.setPixmap(QPixmap(r'D:\python\GUI\ye\1\3.jpg'))
            self.label_4.setPixmap(QPixmap(r'D:\python\GUI\ye\1\4.jpg'))
            self.label_5.setPixmap(QPixmap(r'D:\python\GUI\ye\1\5.jpg'))
            self.label_6.setPixmap(QPixmap(r'D:\python\GUI\ye\1\6.jpg'))
            self.label_7.setPixmap(QPixmap(r'D:\python\GUI\ye\1\7.jpg'))
            self.label_8.setPixmap(QPixmap(r'D:\python\GUI\ye\1\8.jpg'))
            self.label_9.setPixmap(QPixmap(r'D:\python\GUI\ye\1\9.jpg'))
            self.label_10.setPixmap(QPixmap(r'D:\python\GUI\ye\1\10.jpg'))
            self.label_11.setPixmap(QPixmap(r'D:\python\GUI\ye\1\11.jpg'))
            self.label_12.setPixmap(QPixmap(r'D:\python\GUI\ye\1\12.jpg'))
            self.label_13.setPixmap(QPixmap(r'D:\python\GUI\ye\1\13.jpg'))
            self.label_14.setPixmap(QPixmap(r'D:\python\GUI\ye\1\14.jpg'))
            self.label_15.setPixmap(QPixmap(r'D:\python\GUI\ye\1\15.jpg'))
            self.label_16.setPixmap(QPixmap(r'D:\python\GUI\ye\1\16.jpg'))
            self.label_17.setPixmap(QPixmap(r'D:\python\GUI\ye\1\17.jpg'))
            self.label_18.setPixmap(QPixmap(r'D:\python\GUI\ye\1\18.jpg'))
            self.label_19.setPixmap(QPixmap(r'D:\python\GUI\ye\1\19.jpg'))
            self.label_20.setPixmap(QPixmap(r'D:\python\GUI\ye\1\20.jpg'))
            self.label_21.setPixmap(QPixmap(r'D:\python\GUI\ye\1\21.jpg'))
            self.label_22.setPixmap(QPixmap(r'D:\python\GUI\ye\1\22.jpg'))
            self.label_23.setPixmap(QPixmap(r'D:\python\GUI\ye\1\23.jpg'))
            self.label_24.setPixmap(QPixmap(r'D:\python\GUI\ye\1\24.jpg'))
            self.label_25.setPixmap(QPixmap(r'D:\python\GUI\ye\1\25.jpg'))
            self.label_26.setPixmap(QPixmap(r'D:\python\GUI\ye\1\26.jpg'))
            self.label_27.setPixmap(QPixmap(r'D:\python\GUI\ye\1\27.jpg'))
            self.label_28.setPixmap(QPixmap(r'D:\python\GUI\ye\1\28.jpg'))
            self.label_29.setPixmap(QPixmap(r'D:\python\GUI\ye\1\29.jpg'))
            self.label_30.setPixmap(QPixmap(r'D:\python\GUI\ye\1\30.jpg'))
        except:
            pass
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

    def piclist(self, filepath):
        pic_list = []
        j = 0
        for i in os.listdir(filepath):
            if re.match('.*?\.jpg', i):
                pic_list.append(os.path.join(filepath, i))
                print(os.path.join(filepath, i)+str(j))
                j+=1
        return pic_list

    def copy(self):
        r = re.match('复制链接(.*)', self.sender().text())
        index = int(r.group(1))
        clipboard = QApplication.clipboard()
        clipboard.setText(self.links[index-1])

    def download(self):
        self.pushButton.setDisabled(True)
        pages = self.spinBox.text()
        y = Ye(pages)
        y.start(self.progressBar)
        with open(r'D:\python\GUI\ye\1\link.txt', 'r') as f:
            self.links = f.readlines()
        # 加载图片
        pic_list = self.piclist(r'D:\python\GUI\ye\1')
        try:
            self.label_1.setPixmap(QPixmap(r'D:\python\GUI\ye\1\1.jpg'))
            self.label_2.setPixmap(QPixmap(r'D:\python\GUI\ye\1\2.jpg'))
            self.label_3.setPixmap(QPixmap(r'D:\python\GUI\ye\1\3.jpg'))
            self.label_4.setPixmap(QPixmap(r'D:\python\GUI\ye\1\4.jpg'))
            self.label_5.setPixmap(QPixmap(r'D:\python\GUI\ye\1\5.jpg'))
            self.label_6.setPixmap(QPixmap(r'D:\python\GUI\ye\1\6.jpg'))
            self.label_7.setPixmap(QPixmap(r'D:\python\GUI\ye\1\7.jpg'))
            self.label_8.setPixmap(QPixmap(r'D:\python\GUI\ye\1\8.jpg'))
            self.label_9.setPixmap(QPixmap(r'D:\python\GUI\ye\1\9.jpg'))
            self.label_10.setPixmap(QPixmap(r'D:\python\GUI\ye\1\10.jpg'))
            self.label_11.setPixmap(QPixmap(r'D:\python\GUI\ye\1\11.jpg'))
            self.label_12.setPixmap(QPixmap(r'D:\python\GUI\ye\1\12.jpg'))
            self.label_13.setPixmap(QPixmap(r'D:\python\GUI\ye\1\13.jpg'))
            self.label_14.setPixmap(QPixmap(r'D:\python\GUI\ye\1\14.jpg'))
            self.label_15.setPixmap(QPixmap(r'D:\python\GUI\ye\1\15.jpg'))
            self.label_16.setPixmap(QPixmap(r'D:\python\GUI\ye\1\16.jpg'))
            self.label_17.setPixmap(QPixmap(r'D:\python\GUI\ye\1\17.jpg'))
            self.label_18.setPixmap(QPixmap(r'D:\python\GUI\ye\1\18.jpg'))
            self.label_19.setPixmap(QPixmap(r'D:\python\GUI\ye\1\19.jpg'))
            self.label_20.setPixmap(QPixmap(r'D:\python\GUI\ye\1\20.jpg'))
            self.label_21.setPixmap(QPixmap(r'D:\python\GUI\ye\1\21.jpg'))
            self.label_22.setPixmap(QPixmap(r'D:\python\GUI\ye\1\22.jpg'))
            self.label_23.setPixmap(QPixmap(r'D:\python\GUI\ye\1\23.jpg'))
            self.label_24.setPixmap(QPixmap(r'D:\python\GUI\ye\1\24.jpg'))
            self.label_25.setPixmap(QPixmap(r'D:\python\GUI\ye\1\25.jpg'))
            self.label_26.setPixmap(QPixmap(r'D:\python\GUI\ye\1\26.jpg'))
            self.label_27.setPixmap(QPixmap(r'D:\python\GUI\ye\1\27.jpg'))
            self.label_28.setPixmap(QPixmap(r'D:\python\GUI\ye\1\28.jpg'))
            self.label_29.setPixmap(QPixmap(r'D:\python\GUI\ye\1\29.jpg'))
            self.label_30.setPixmap(QPixmap(r'D:\python\GUI\ye\1\30.jpg'))
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
        except:
            pass
        self.pushButton.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyForm = MyForm()
    MyForm.show()
    sys.exit(app.exec_())