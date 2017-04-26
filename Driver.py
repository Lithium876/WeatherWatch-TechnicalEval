from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
from Forcaster import *
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(644, 434)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.locationComboBox = QtGui.QComboBox(self.centralwidget)
        self.locationComboBox.setGeometry(QtCore.QRect(450, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.locationComboBox.setFont(font)
        self.locationComboBox.setObjectName(_fromUtf8("locationComboBox"))
        self.locationComboBox.setFont(font)
        self.locationComboBox.addItem("Kingston")
        self.locationComboBox.addItem("Spanish Town")
        self.locationComboBox.addItem("Portmore")
        self.locationComboBox.addItem("Morant Bay")
        self.locationComboBox.addItem("Port Antonio")
        self.locationComboBox.addItem("Port Maria")
        self.locationComboBox.addItem("Ocho Rios")
        self.locationComboBox.addItem("Falmouth")
        self.locationComboBox.addItem("Montego Bay")
        self.locationComboBox.addItem("Negril")
        self.locationComboBox.addItem("Savanna-la-mar")
        self.locationComboBox.addItem("Santa Cruz")
        self.locationComboBox.addItem("Mandeville")
        self.locationComboBox.addItem("May Pen")

        self.locationLabel = QtGui.QLabel(self.centralwidget)
        self.locationLabel.setGeometry(QtCore.QRect(380, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.locationLabel.setFont(font)
        self.locationLabel.setObjectName(_fromUtf8("locationLabel"))
        
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 200, 621, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        
        self.displayCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.displayCheckBox.setGeometry(QtCore.QRect(380, 60, 141, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.displayCheckBox.setFont(font)
        self.displayCheckBox.setObjectName(_fromUtf8("displayCheckBox"))
        self.displayCheckBox.setChecked(True)
        
        self.emailCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.emailCheckBox.setGeometry(QtCore.QRect(380, 90, 121, 17))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.emailCheckBox.setFont(font)
        self.emailCheckBox.setObjectName(_fromUtf8("emailCheckBox"))
        
        self.button = QtGui.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(380, 160, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button.setFont(font)
        self.button.setObjectName(_fromUtf8("button"))
        self.button.clicked.connect(self.getForecast)
        
        self.emailComboBox = QtGui.QComboBox(self.centralwidget)
        self.emailComboBox.setEnabled(False)
        self.emailComboBox.setGeometry(QtCore.QRect(380, 120, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.emailComboBox.setFont(font)
        self.emailCheckBox.stateChanged.connect(self.enable)
        self.emailComboBox.setObjectName(_fromUtf8("emailComboBox"))
        self.emailComboBox.addItem("Will Rain - IT Staff only")
        self.emailComboBox.addItem("Will Rain - General Staff only")
        self.emailComboBox.addItem("Will Rain - IT Staff and General Staff")
        self.emailComboBox.addItem("Will Not Rain - General Staff")

        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 220, 621, 181))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableWidget.setFont(font)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.calendarWidget = QtGui.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 371, 191))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))

        MainWindow.setCentralWidget(self.centralwidget)

        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 644, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOpen_Email_File = QtGui.QMenu(self.menuFile)
        self.menuOpen_Email_File.setObjectName(_fromUtf8("menuOpen_Email_File"))
        
        MainWindow.setMenuBar(self.menuBar)
       
        self.actionWill_Rain_IT_Staff = QtGui.QAction(MainWindow)
        self.actionWill_Rain_IT_Staff.setObjectName(_fromUtf8("actionWill_Rain_IT_Staff"))
        self.actionWill_Rain_General_Staff = QtGui.QAction(MainWindow)
        self.actionWill_Rain_General_Staff.setObjectName(_fromUtf8("actionWill_Rain_General_Staff"))
        self.actionWill_Not_Rain_General_Staff = QtGui.QAction(MainWindow)
        self.actionWill_Not_Rain_General_Staff.setObjectName(_fromUtf8("actionWill_Not_Rain_General_Staff"))
        
        self.actionExit_2 = QtGui.QAction(MainWindow)
        self.actionExit_2.setObjectName(_fromUtf8("actionExit_2"))
        
        self.actionSupported_Locations = QtGui.QAction(MainWindow)
        self.actionSupported_Locations.setObjectName(_fromUtf8("actionSupported_Locations"))
        
        self.menuOpen_Email_File.addAction(self.actionWill_Rain_IT_Staff)
        self.menuOpen_Email_File.addAction(self.actionWill_Rain_General_Staff)
        self.menuOpen_Email_File.addAction(self.actionWill_Not_Rain_General_Staff)
        
        self.menuFile.addAction(self.menuOpen_Email_File.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit_2, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.actionWill_Rain_IT_Staff, QtCore.SIGNAL(_fromUtf8("triggered()")), self.Will_Rain_IT_Staff)
        QtCore.QObject.connect(self.actionWill_Rain_General_Staff, QtCore.SIGNAL(_fromUtf8("triggered()")), self.Will_Rain_General_Staff)
        QtCore.QObject.connect(self.actionWill_Not_Rain_General_Staff, QtCore.SIGNAL(_fromUtf8("triggered()")), self.Not_Rain_General_Staff)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Forcaster", None))
        self.locationLabel.setText(_translate("MainWindow", "Location:", None))
        self.displayCheckBox.setText(_translate("MainWindow", "Display Forecast", None))
        self.emailCheckBox.setText(_translate("MainWindow", "Send Email", None))
        self.button.setText(_translate("MainWindow", "Get Forecast", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "DayTime", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Temperature", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Rainfall", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Pressure", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Wind Speed", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Wind Direction", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuOpen_Email_File.setTitle(_translate("MainWindow", "Open Email File", None))
        self.actionWill_Rain_IT_Staff.setText(_translate("MainWindow", "Will Rain - IT Staff", None))
        self.actionWill_Rain_General_Staff.setText(_translate("MainWindow", "Will Rain - General Staff", None))
        self.actionWill_Not_Rain_General_Staff.setText(_translate("MainWindow", "Will Not Rain - General Staff", None))
        self.actionExit_2.setText(_translate("MainWindow", "Exit", None))

    def enable(self):
        if self.emailCheckBox.isChecked():
            self.emailComboBox.setEnabled(True)
        else:
            self.emailComboBox.setEnabled(False)

    @staticmethod
    def showMessage(statusMsg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(statusMsg)
        if "No" in statusMsg:
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
        elif "Error" in statusMsg:
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Sending Email Error")
        else:
            msg.setWindowTitle("Email Sent!")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def getForecast(self):
        if self.displayCheckBox.isChecked():
            location = WeatherForcast(str(self.locationComboBox.currentText()))
            location.getForcast()
            data = location.displayForcast()
            for x in range(0,len(data)):
                self.tableWidget.setItem(0, x, QTableWidgetItem(data[x]))

        if self.emailCheckBox.isChecked():
            recievers = str(self.emailComboBox.currentText())
            if location.willHaveRainTomorrow():
                Email_Subject = "Schedule Change"
                if "IT Staff only" in recievers:
                    msg = location.sendEmail(Email_Subject, True, "IT Staff")
                elif "General Staff only" in recievers:
                    msg = location.sendEmail(Email_Subject, True)
                elif "IT Staff and General Staff" in recievers:
                    msg = location.sendEmail(Email_Subject, True, "IT Staff")
                    msg = location.sendEmail(Email_Subject, True)
            else:
                Email_Subject = "Schedule Remains"
                msg = location.sendEmail(Email_Subject)
            self.showMessage(msg)

    @staticmethod
    def Not_Rain_General_Staff():
        os.system("notepad.exe NoRainEmail.txt")

    @staticmethod
    def Will_Rain_General_Staff():
        os.system("notepad.exe RainEmail.txt")

    @staticmethod
    def Will_Rain_IT_Staff():
        os.system("notepad.exe ITStaffEmail.txt")

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
