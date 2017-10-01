# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Nov 18 17:47:47 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        MainWindow.resize(418, 212)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.one_tab = QtGui.QWidget()
        self.one_tab.setObjectName(_fromUtf8("one_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.one_tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.one_vrml_button = QtGui.QPushButton(self.one_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.one_vrml_button.setIcon(icon)
        self.one_vrml_button.setObjectName(_fromUtf8("one_vrml_button"))
        self.gridLayout.addWidget(self.one_vrml_button, 0, 0, 1, 1)
        self.one_vrml_input = QtGui.QLineEdit(self.one_tab)
        self.one_vrml_input.setObjectName(_fromUtf8("one_vrml_input"))
        self.gridLayout.addWidget(self.one_vrml_input, 0, 1, 1, 1)
        self.one_csv_button = QtGui.QPushButton(self.one_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save"))
        self.one_csv_button.setIcon(icon)
        self.one_csv_button.setObjectName(_fromUtf8("one_csv_button"))
        self.gridLayout.addWidget(self.one_csv_button, 1, 0, 1, 1)
        self.one_csv_input = QtGui.QLineEdit(self.one_tab)
        self.one_csv_input.setObjectName(_fromUtf8("one_csv_input"))
        self.gridLayout.addWidget(self.one_csv_input, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.one_run_button = QtGui.QPushButton(self.one_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("media-playback-start"))
        self.one_run_button.setIcon(icon)
        self.one_run_button.setObjectName(_fromUtf8("one_run_button"))
        self.verticalLayout_2.addWidget(self.one_run_button)
        self.tabWidget.addTab(self.one_tab, _fromUtf8(""))
        self.many_tab = QtGui.QWidget()
        self.many_tab.setObjectName(_fromUtf8("many_tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.many_tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.many_vrml_input = QtGui.QLineEdit(self.many_tab)
        self.many_vrml_input.setObjectName(_fromUtf8("many_vrml_input"))
        self.gridLayout_2.addWidget(self.many_vrml_input, 0, 1, 1, 1)
        self.many_csv_input = QtGui.QLineEdit(self.many_tab)
        self.many_csv_input.setObjectName(_fromUtf8("many_csv_input"))
        self.gridLayout_2.addWidget(self.many_csv_input, 2, 1, 1, 1)
        self.many_vrml_button = QtGui.QPushButton(self.many_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-open"))
        self.many_vrml_button.setIcon(icon)
        self.many_vrml_button.setObjectName(_fromUtf8("many_vrml_button"))
        self.gridLayout_2.addWidget(self.many_vrml_button, 0, 0, 1, 1)
        self.many_csv_button = QtGui.QPushButton(self.many_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("document-save"))
        self.many_csv_button.setIcon(icon)
        self.many_csv_button.setObjectName(_fromUtf8("many_csv_button"))
        self.gridLayout_2.addWidget(self.many_csv_button, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.many_run_button = QtGui.QPushButton(self.many_tab)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("media-playback-start"))
        self.many_run_button.setIcon(icon)
        self.many_run_button.setObjectName(_fromUtf8("many_run_button"))
        self.verticalLayout_3.addWidget(self.many_run_button)
        self.tabWidget.addTab(self.many_tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 418, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AreasCBB", None))
        self.one_vrml_button.setText(_translate("MainWindow", "Open ...", None))
        self.one_vrml_input.setPlaceholderText(_translate("MainWindow", "input - VRML file", None))
        self.one_csv_button.setText(_translate("MainWindow", "Save ...", None))
        self.one_csv_input.setPlaceholderText(_translate("MainWindow", "ouput - CSV file ", None))
        self.one_run_button.setText(_translate("MainWindow", "Compute Areas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.one_tab), _translate("MainWindow", "Area from one VMRL", None))
        self.many_vrml_input.setPlaceholderText(_translate("MainWindow", "Folder with many VRMLs", None))
        self.many_csv_input.setPlaceholderText(_translate("MainWindow", "Folder to save many CSVs ", None))
        self.many_vrml_button.setText(_translate("MainWindow", "Open Folder...", None))
        self.many_csv_button.setText(_translate("MainWindow", "Save Folder...", None))
        self.many_run_button.setText(_translate("MainWindow", "Compute Areas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.many_tab), _translate("MainWindow", "Area from many VMRLs", None))
        self.action_Quit.setText(_translate("MainWindow", "&Quit", None))

