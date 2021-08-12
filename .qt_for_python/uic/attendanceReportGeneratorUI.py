# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\OneDrive\project\webScrapper\attendanceReportGenerator\attendanceReportGeneratorUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(526, 354)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(16, 180, 111, 19))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.leFilePath = QtWidgets.QLineEdit(self.centralwidget)
        self.leFilePath.setGeometry(QtCore.QRect(130, 180, 281, 20))
        self.leFilePath.setObjectName("leFilePath")
        self.pbBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.pbBrowse.setGeometry(QtCore.QRect(420, 180, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.pbBrowse.setFont(font)
        self.pbBrowse.setObjectName("pbBrowse")
        self.pbGen = QtWidgets.QPushButton(self.centralwidget)
        self.pbGen.setGeometry(QtCore.QRect(20, 260, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.pbGen.setFont(font)
        self.pbGen.setObjectName("pbGen")
        self.pbStop = QtWidgets.QPushButton(self.centralwidget)
        self.pbStop.setGeometry(QtCore.QRect(160, 260, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.pbStop.setFont(font)
        self.pbStop.setObjectName("pbStop")
        self.pbExit = QtWidgets.QPushButton(self.centralwidget)
        self.pbExit.setGeometry(QtCore.QRect(420, 260, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.pbExit.setFont(font)
        self.pbExit.setObjectName("pbExit")
        self.pbSend = QtWidgets.QPushButton(self.centralwidget)
        self.pbSend.setGeometry(QtCore.QRect(290, 260, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.pbSend.setFont(font)
        self.pbSend.setObjectName("pbSend")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(30, 110, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(250, 110, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.cbAcademicYear = QtWidgets.QComboBox(self.centralwidget)
        self.cbAcademicYear.setGeometry(QtCore.QRect(140, 110, 69, 22))
        self.cbAcademicYear.setObjectName("cbAcademicYear")
        self.cbAcademicYear.addItem("")
        self.cbSem = QtWidgets.QComboBox(self.centralwidget)
        self.cbSem.setGeometry(QtCore.QRect(350, 110, 69, 22))
        self.cbSem.setObjectName("cbSem")
        self.cbSem.addItem("")
        self.leUserName = QtWidgets.QLineEdit(self.centralwidget)
        self.leUserName.setGeometry(QtCore.QRect(110, 10, 113, 20))
        self.leUserName.setObjectName("leUserName")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 10, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lePassword = QtWidgets.QLineEdit(self.centralwidget)
        self.lePassword.setGeometry(QtCore.QRect(110, 50, 113, 20))
        self.lePassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lePassword.setObjectName("lePassword")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 50, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 220, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.cbStudentID = QtWidgets.QComboBox(self.centralwidget)
        self.cbStudentID.setGeometry(QtCore.QRect(130, 220, 171, 22))
        self.cbStudentID.setEditable(False)
        self.cbStudentID.setObjectName("cbStudentID")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 290, 491, 23))
        self.progressBar.setProperty("value", 10)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 0, 151, 20))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.teGreetings = QtWidgets.QTextEdit(self.centralwidget)
        self.teGreetings.setGeometry(QtCore.QRect(280, 20, 231, 71))
        self.teGreetings.setObjectName("teGreetings")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 526, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Studen List File:"))
        self.pbBrowse.setText(_translate("MainWindow", "Browse"))
        self.pbGen.setText(_translate("MainWindow", "Generate"))
        self.pbStop.setText(_translate("MainWindow", "Stop"))
        self.pbExit.setText(_translate("MainWindow", "Exit"))
        self.pbSend.setText(_translate("MainWindow", "Send"))
        self.label_9.setText(_translate("MainWindow", "Academic Year"))
        self.label_8.setText(_translate("MainWindow", "Semester"))
        self.cbAcademicYear.setItemText(0, _translate("MainWindow", "2021-2022"))
        self.cbSem.setItemText(0, _translate("MainWindow", "Odd Sem"))
        self.label_2.setText(_translate("MainWindow", "User Name"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.label_4.setText(_translate("MainWindow", "Current ID"))
        self.label_5.setText(_translate("MainWindow", "Message Greetings"))
        self.teGreetings.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Dear Parent/Guardian</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Greetings from KLH ECE Department</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please find the weekly attendance summary of your child/ward</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please contact your child\'s/ward\'s mentor for any clarification or suggestion</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))