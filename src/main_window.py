# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(543, 309)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 9)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.one_vrml_tab = QtWidgets.QWidget()
        self.one_vrml_tab.setObjectName("one_vrml_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.one_vrml_tab)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.one_vrml_button = QtWidgets.QPushButton(self.one_vrml_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.one_vrml_button.sizePolicy().hasHeightForWidth())
        self.one_vrml_button.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.one_vrml_button.setIcon(icon)
        self.one_vrml_button.setObjectName("one_vrml_button")
        self.gridLayout.addWidget(self.one_vrml_button, 0, 0, 1, 1)
        self.one_vrml_input = QtWidgets.QLineEdit(self.one_vrml_tab)
        self.one_vrml_input.setObjectName("one_vrml_input")
        self.gridLayout.addWidget(self.one_vrml_input, 0, 1, 1, 1)
        self.one_vrml_csv_button = QtWidgets.QPushButton(self.one_vrml_tab)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.one_vrml_csv_button.setIcon(icon)
        self.one_vrml_csv_button.setObjectName("one_vrml_csv_button")
        self.gridLayout.addWidget(self.one_vrml_csv_button, 1, 0, 1, 1)
        self.one_vrml_csv_input = QtWidgets.QLineEdit(self.one_vrml_tab)
        self.one_vrml_csv_input.setObjectName("one_vrml_csv_input")
        self.gridLayout.addWidget(self.one_vrml_csv_input, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.one_vrml_run_button = QtWidgets.QPushButton(self.one_vrml_tab)
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.one_vrml_run_button.setIcon(icon)
        self.one_vrml_run_button.setObjectName("one_vrml_run_button")
        self.verticalLayout_2.addWidget(self.one_vrml_run_button)
        self.tabWidget.addTab(self.one_vrml_tab, "")
        self.many_vrml_tab = QtWidgets.QWidget()
        self.many_vrml_tab.setObjectName("many_vrml_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.many_vrml_tab)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.many_vrml_input = QtWidgets.QLineEdit(self.many_vrml_tab)
        self.many_vrml_input.setObjectName("many_vrml_input")
        self.gridLayout_2.addWidget(self.many_vrml_input, 0, 1, 1, 1)
        self.many_vrml_csv_input = QtWidgets.QLineEdit(self.many_vrml_tab)
        self.many_vrml_csv_input.setObjectName("many_vrml_csv_input")
        self.gridLayout_2.addWidget(self.many_vrml_csv_input, 2, 1, 1, 1)
        self.many_vrml_button = QtWidgets.QPushButton(self.many_vrml_tab)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.many_vrml_button.setIcon(icon)
        self.many_vrml_button.setObjectName("many_vrml_button")
        self.gridLayout_2.addWidget(self.many_vrml_button, 0, 0, 1, 1)
        self.many_vrml_csv_button = QtWidgets.QPushButton(self.many_vrml_tab)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.many_vrml_csv_button.setIcon(icon)
        self.many_vrml_csv_button.setObjectName("many_vrml_csv_button")
        self.gridLayout_2.addWidget(self.many_vrml_csv_button, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.many_vrml_run_button = QtWidgets.QPushButton(self.many_vrml_tab)
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.many_vrml_run_button.setIcon(icon)
        self.many_vrml_run_button.setObjectName("many_vrml_run_button")
        self.verticalLayout_3.addWidget(self.many_vrml_run_button)
        self.tabWidget.addTab(self.many_vrml_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(-1, 0, -1, 0)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.outputFormatLabel = QtWidgets.QLabel(self.centralWidget)
        self.outputFormatLabel.setObjectName("outputFormatLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.outputFormatLabel)
        self.outputFormatComboBox = QtWidgets.QComboBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputFormatComboBox.sizePolicy().hasHeightForWidth())
        self.outputFormatComboBox.setSizePolicy(sizePolicy)
        self.outputFormatComboBox.setObjectName("outputFormatComboBox")
        self.outputFormatComboBox.addItem("")
        self.outputFormatComboBox.addItem("")
        self.outputFormatComboBox.addItem("")
        self.outputFormatComboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.outputFormatComboBox)
        self.exportResolutionLabel = QtWidgets.QLabel(self.centralWidget)
        self.exportResolutionLabel.setObjectName("exportResolutionLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.exportResolutionLabel)
        self.exportReductionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportReductionDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.exportReductionDoubleSpinBox.setSizePolicy(sizePolicy)
        self.exportReductionDoubleSpinBox.setMinimum(10.0)
        self.exportReductionDoubleSpinBox.setProperty("value", 30.0)
        self.exportReductionDoubleSpinBox.setObjectName("exportReductionDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.exportReductionDoubleSpinBox)
        self.cleanVrmlLabel = QtWidgets.QLabel(self.centralWidget)
        self.cleanVrmlLabel.setObjectName("cleanVrmlLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.cleanVrmlLabel)
        self.cleanVrmlCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.cleanVrmlCheckBox.setEnabled(True)
        self.cleanVrmlCheckBox.setChecked(True)
        self.cleanVrmlCheckBox.setObjectName("cleanVrmlCheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cleanVrmlCheckBox)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.precisionLabel = QtWidgets.QLabel(self.centralWidget)
        self.precisionLabel.setObjectName("precisionLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.precisionLabel)
        self.precisionSpinBox = QtWidgets.QSpinBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.precisionSpinBox.sizePolicy().hasHeightForWidth())
        self.precisionSpinBox.setSizePolicy(sizePolicy)
        self.precisionSpinBox.setMinimum(1)
        self.precisionSpinBox.setMaximum(200)
        self.precisionSpinBox.setProperty("value", 50)
        self.precisionSpinBox.setObjectName("precisionSpinBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.precisionSpinBox)
        self.includeSegmentsLabel = QtWidgets.QLabel(self.centralWidget)
        self.includeSegmentsLabel.setObjectName("includeSegmentsLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.includeSegmentsLabel)
        self.includeSegmentsCheckBox = QtWidgets.QCheckBox(self.centralWidget)
        self.includeSegmentsCheckBox.setObjectName("includeSegmentsCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.includeSegmentsCheckBox)
        self.kernelSizeLabel = QtWidgets.QLabel(self.centralWidget)
        self.kernelSizeLabel.setObjectName("kernelSizeLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.kernelSizeLabel)
        self.kernelSizeSpinBox = QtWidgets.QSpinBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kernelSizeSpinBox.sizePolicy().hasHeightForWidth())
        self.kernelSizeSpinBox.setSizePolicy(sizePolicy)
        self.kernelSizeSpinBox.setProperty("value", 3)
        self.kernelSizeSpinBox.setObjectName("kernelSizeSpinBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.kernelSizeSpinBox)
        self.horizontalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 543, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AreasCBB"))
        self.one_vrml_button.setText(_translate("MainWindow", "Open ..."))
        self.one_vrml_input.setPlaceholderText(_translate("MainWindow", "input - VRML file"))
        self.one_vrml_csv_button.setText(_translate("MainWindow", "Save ..."))
        self.one_vrml_csv_input.setPlaceholderText(_translate("MainWindow", "output - CSV file "))
        self.one_vrml_run_button.setText(_translate("MainWindow", "Compute Areas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.one_vrml_tab), _translate("MainWindow", "Area from one file"))
        self.many_vrml_input.setPlaceholderText(_translate("MainWindow", "Folder with many VRMLs"))
        self.many_vrml_csv_input.setPlaceholderText(_translate("MainWindow", "Folder to save many CSVs "))
        self.many_vrml_button.setText(_translate("MainWindow", "Open Folder..."))
        self.many_vrml_csv_button.setText(_translate("MainWindow", "Save Folder..."))
        self.many_vrml_run_button.setText(_translate("MainWindow", "Compute Areas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.many_vrml_tab), _translate("MainWindow", "Area from many files"))
        self.outputFormatLabel.setText(_translate("MainWindow", "OutputFormat"))
        self.outputFormatComboBox.setItemText(0, _translate("MainWindow", "None"))
        self.outputFormatComboBox.setItemText(1, _translate("MainWindow", "Obj"))
        self.outputFormatComboBox.setItemText(2, _translate("MainWindow", "Stl"))
        self.outputFormatComboBox.setItemText(3, _translate("MainWindow", "Vrml"))
        self.exportResolutionLabel.setText(_translate("MainWindow", "OutputMeshResolutionPercentage"))
        self.cleanVrmlLabel.setText(_translate("MainWindow", "Clean Vrml"))
        self.precisionLabel.setText(_translate("MainWindow", "Precision"))
        self.includeSegmentsLabel.setText(_translate("MainWindow", "Include Segments"))
        self.kernelSizeLabel.setText(_translate("MainWindow", "KernelSize"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))

