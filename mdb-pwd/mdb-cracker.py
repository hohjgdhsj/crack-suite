#/bin/bash/python
#coding=utf-8
#le4f.net

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class PYAccess(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(397, 91)
        MainWindow.setMaximumSize(QtCore.QSize(397, 91))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Access.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.btnSelectFile = QtGui.QPushButton(self.centralWidget)
        self.btnSelectFile.setGeometry(QtCore.QRect(290, 20, 91, 23))
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.tbFilePath = QtGui.QLineEdit(self.centralWidget)
        self.tbFilePath.setGeometry(QtCore.QRect(20, 20, 261, 20))
        self.tbFilePath.setObjectName(_fromUtf8("tbFilePath"))
        self.tbVersion = QtGui.QLineEdit(self.centralWidget)
        self.tbVersion.setGeometry(QtCore.QRect(20, 50, 111, 20))
        self.tbVersion.setObjectName(_fromUtf8("tbVersion"))
        self.tbPassword = QtGui.QLineEdit(self.centralWidget)
        self.tbPassword.setGeometry(QtCore.QRect(160, 50, 221, 20))
        self.tbPassword.setObjectName(_fromUtf8("tbPassword"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.btnSelectFile, QtCore.SIGNAL(_fromUtf8("clicked()")), self.slotselectfile)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def slotselectfile(self):
        fname = QtGui.QFileDialog.getOpenFileName(MainWindow, 'Open Access File','/*.mdb')
        if fname=='':
            return
        else:
            self.tbFilePath.setText(fname)
            baseByte=[0xbe, 0xec, 0x65, 0x9c, 0xfe,0x28, 0x2b, 0x8a, 0x6c, 0x7b,0xcd, 0xdf, 0x4f, 0x13, 0xf7,0xb1]
            flagByte = 0x0c
            password = '';
            fs=open(fname,'r')
            fs.seek(0x14)
            version='unknow'
            ver = ord(fs.read(1))
            if ver==1:
                version='Access2000'
            elif ver==0:
                version='Access97'
            fs.seek(0x42)
            bs=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            integer = 0
            while integer < 33:
                tmpInt=ord(fs.read(1))
                bs[integer]=tmpInt
                integer=integer+1
            flag = bs[32] ^ flagByte
            i = 0
            while i < 16:
                b = (baseByte[i] ^ bs[i * 2])
                if i % 2 == 0 and ver == 1:
                    b = b^flag;
                if b > 0 :
                    password = password + chr(b)
                i=i+1
            fs.close()
            self.tbVersion.setText(version)
            self.tbPassword.setText(password)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MDB-Cracker", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectFile.setText(QtGui.QApplication.translate("MainWindow", " Select File..", None, QtGui.QApplication.UnicodeUTF8))
        self.tbFilePath.setText(QtGui.QApplication.translate("MainWindow", "PATH", None, QtGui.QApplication.UnicodeUTF8))
        self.tbVersion.setText(QtGui.QApplication.translate("MainWindow", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.tbPassword.setText(QtGui.QApplication.translate("MainWindow", "MDBFile Password:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = PYAccess()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())