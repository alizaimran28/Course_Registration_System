# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\University\Semester 6\Software Construction and Development\Project\HelpStudent.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_helpStudent(object):
    def setupUi(self, helpStudent):
        helpStudent.setObjectName("helpStudent")
        helpStudent.resize(460, 410)
        self.centralwidget = QtWidgets.QWidget(helpStudent)
        self.centralwidget.setObjectName("centralwidget")
        self.RegisterCourse = QtWidgets.QWidget(self.centralwidget)
        self.RegisterCourse.setEnabled(True)
        self.RegisterCourse.setGeometry(QtCore.QRect(0, 0, 471, 391))
        self.RegisterCourse.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RegisterCourse.setInputMethodHints(QtCore.Qt.ImhNone)
        self.RegisterCourse.setObjectName("RegisterCourse")
        self.CourseName = QtWidgets.QLineEdit(self.RegisterCourse)
        self.CourseName.setGeometry(QtCore.QRect(72, 120, 331, 41))
        self.CourseName.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.CourseName.setObjectName("CourseName")
        self.CourseNamelabel = QtWidgets.QLabel(self.RegisterCourse)
        self.CourseNamelabel.setGeometry(QtCore.QRect(70, 90, 121, 21))
        self.CourseNamelabel.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";")
        self.CourseNamelabel.setObjectName("CourseNamelabel")
        self.CourseIDlabel = QtWidgets.QLabel(self.RegisterCourse)
        self.CourseIDlabel.setGeometry(QtCore.QRect(70, 200, 121, 21))
        self.CourseIDlabel.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";")
        self.CourseIDlabel.setObjectName("CourseIDlabel")
        self.messagealert = QtWidgets.QLabel(self.RegisterCourse)
        self.messagealert.setGeometry(QtCore.QRect(70, 310, 321, 21))
        self.messagealert.setText("")
        self.messagealert.setObjectName("messagealert")
        self.label_2 = QtWidgets.QLabel(self.RegisterCourse)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 231, 31))
        self.label_2.setStyleSheet("font: 63 14pt \"Sitka Display Semibold\";\n"
"background-color: rgb(66, 167, 255);")
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(self.RegisterCourse)
        self.widget.setGeometry(QtCore.QRect(0, 0, 461, 81))
        self.widget.setStyleSheet("background-color: rgb(66, 167, 255);")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.RegisterCourse)
        self.label.setGeometry(QtCore.QRect(70, 170, 331, 16))
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.RegisterCourse)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 331, 31))
        self.label_3.setStyleSheet("font: 75 12pt \"Arial\";")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.RegisterCourse)
        self.pushButton.setGeometry(QtCore.QRect(180, 270, 101, 31))
        self.pushButton.setStyleSheet("background-color: rgb(66, 167, 255);")
        self.pushButton.setObjectName("pushButton")
        self.backbtn = QtWidgets.QPushButton(self.RegisterCourse)
        self.backbtn.setGeometry(QtCore.QRect(20, 340, 61, 23))
        self.backbtn.setObjectName("backbtn")
        self.label_4 = QtWidgets.QLabel(self.RegisterCourse)
        self.label_4.setGeometry(QtCore.QRect(130, 340, 181, 16))
        self.label_4.setObjectName("label_4")
        self.click = QtWidgets.QPushButton(self.RegisterCourse)
        self.click.setGeometry(QtCore.QRect(310, 340, 61, 23))
        self.click.setStyleSheet("background-color: rgb(66, 167, 255);")
        self.click.setObjectName("click")
        self.widget.raise_()
        self.CourseName.raise_()
        self.CourseIDlabel.raise_()
        self.messagealert.raise_()
        self.label_2.raise_()
        self.CourseNamelabel.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.pushButton.raise_()
        self.backbtn.raise_()
        self.label_4.raise_()
        self.click.raise_()
        helpStudent.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(helpStudent)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 460, 21))
        self.menubar.setObjectName("menubar")
        helpStudent.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(helpStudent)
        self.statusbar.setObjectName("statusbar")
        helpStudent.setStatusBar(self.statusbar)

        self.retranslateUi(helpStudent)
        QtCore.QMetaObject.connectSlotsByName(helpStudent)

    def retranslateUi(self, helpStudent):
        _translate = QtCore.QCoreApplication.translate
        helpStudent.setWindowTitle(_translate("helpStudent", "MainWindow"))
        self.CourseNamelabel.setText(_translate("helpStudent", "Course Name:"))
        self.CourseIDlabel.setText(_translate("helpStudent", "Course ID:"))
        self.label_2.setText(_translate("helpStudent", "Student Registration Form"))
        self.label.setText(_translate("helpStudent", "Note: Enter course name to know its ID"))
        self.pushButton.setText(_translate("helpStudent", "GET ID"))
        self.backbtn.setText(_translate("helpStudent", "<<Back"))
        self.label_4.setText(_translate("helpStudent", "click here get know about all courses"))
        self.click.setText(_translate("helpStudent", "click here"))
