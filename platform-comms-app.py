# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'platform-comms-app.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(670, 443)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 251))
        self.groupBox.setMaximumSize(QtCore.QSize(999999, 16777215))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lblTelecommandN = QtWidgets.QLabel(self.groupBox)
        self.lblTelecommandN.setObjectName("lblTelecommandN")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTelecommandN)
        self.inputTelecommandN = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTelecommandN.sizePolicy().hasHeightForWidth())
        self.inputTelecommandN.setSizePolicy(sizePolicy)
        self.inputTelecommandN.setObjectName("inputTelecommandN")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputTelecommandN)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 5, 0, 1, 3, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(9, 29, 128, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 60, 377, 38))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_4.addWidget(self.pushButton_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget)
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout_2.addWidget(self.dateEdit, 0, QtCore.Qt.AlignLeft)
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.horizontalLayout_2.addWidget(self.dateTimeEdit)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.gridLayout_5.addLayout(self.formLayout_3, 0, 0, 1, 1)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_8)
        self.gridLayout_5.addLayout(self.formLayout_7, 0, 1, 1, 1)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_6)
        self.gridLayout_5.addLayout(self.formLayout_8, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 6, 0, 1, 3)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_3.addWidget(self.checkBox, 1, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 0, 2, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.lblTelecommandData = QtWidgets.QLabel(self.groupBox)
        self.lblTelecommandData.setObjectName("lblTelecommandData")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTelecommandData)
        self.inputTelecommandData = QtWidgets.QLineEdit(self.groupBox)
        self.inputTelecommandData.setObjectName("inputTelecommandData")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputTelecommandData)
        self.gridLayout_3.addLayout(self.formLayout_2, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab, "")
        self.tabTelecommanding = QtWidgets.QWidget()
        self.tabTelecommanding.setObjectName("tabTelecommanding")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabTelecommanding)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tabTelecommanding)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 251))
        self.groupBox_4.setMaximumSize(QtCore.QSize(999999, 16777215))
        self.groupBox_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_9)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(self.groupBox_6)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_6.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.label_14 = QtWidgets.QLabel(self.groupBox_6)
        self.label_14.setObjectName("label_14")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_14)
        self.gridLayout_6.addLayout(self.formLayout_10, 0, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 0, 5, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_6.addWidget(self.checkBox_3, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tabTelecommanding, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 251))
        self.groupBox_5.setMaximumSize(QtCore.QSize(999999, 16777215))
        self.groupBox_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.formLayout_12 = QtWidgets.QFormLayout()
        self.formLayout_12.setObjectName("formLayout_12")
        self.lblTelecommandData_2 = QtWidgets.QLabel(self.groupBox_5)
        self.lblTelecommandData_2.setObjectName("lblTelecommandData_2")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTelecommandData_2)
        self.inputTelecommandData_2 = QtWidgets.QLineEdit(self.groupBox_5)
        self.inputTelecommandData_2.setObjectName("inputTelecommandData_2")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputTelecommandData_2)
        self.gridLayout_4.addLayout(self.formLayout_12, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_4.addWidget(self.pushButton_4, 5, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_5.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_5.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_5.setObjectName("formLayout_5")
        self.lblTelecommandN_2 = QtWidgets.QLabel(self.groupBox_5)
        self.lblTelecommandN_2.setObjectName("lblTelecommandN_2")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTelecommandN_2)
        self.inputTelecommandN_2 = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTelecommandN_2.sizePolicy().hasHeightForWidth())
        self.inputTelecommandN_2.setSizePolicy(sizePolicy)
        self.inputTelecommandN_2.setObjectName("inputTelecommandN_2")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputTelecommandN_2)
        self.gridLayout_4.addLayout(self.formLayout_5, 0, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_7.setObjectName("groupBox_7")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_6.setGeometry(QtCore.QRect(9, 29, 128, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_7)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 60, 377, 38))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_5.addWidget(self.pushButton_7)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.layoutWidget_2)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.horizontalLayout_3.addWidget(self.dateEdit_2, 0, QtCore.Qt.AlignLeft)
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.layoutWidget_2)
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.horizontalLayout_3.addWidget(self.dateTimeEdit_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        self.label_10.setObjectName("label_10")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.label_11 = QtWidgets.QLabel(self.groupBox_8)
        self.label_11.setObjectName("label_11")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_11)
        self.gridLayout_7.addLayout(self.formLayout_6, 0, 0, 1, 1)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_12 = QtWidgets.QLabel(self.groupBox_8)
        self.label_12.setObjectName("label_12")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_15 = QtWidgets.QLabel(self.groupBox_8)
        self.label_15.setObjectName("label_15")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_15)
        self.gridLayout_7.addLayout(self.formLayout_9, 0, 1, 1, 1)
        self.formLayout_11 = QtWidgets.QFormLayout()
        self.formLayout_11.setObjectName("formLayout_11")
        self.label_16 = QtWidgets.QLabel(self.groupBox_8)
        self.label_16.setObjectName("label_16")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.label_17 = QtWidgets.QLabel(self.groupBox_8)
        self.label_17.setObjectName("label_17")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_17)
        self.gridLayout_7.addLayout(self.formLayout_11, 1, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox_8)
        self.gridLayout_4.addLayout(self.verticalLayout_6, 6, 0, 1, 2)
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_4.addWidget(self.pushButton_8, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.widget, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_3)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 20, 401, 181))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.cb_serialPortSelection = QtWidgets.QComboBox(self.tab_3)
        self.cb_serialPortSelection.setGeometry(QtCore.QRect(480, 80, 151, 22))
        self.cb_serialPortSelection.setObjectName("cb_serialPortSelection")
        self.tabWidget.addTab(self.tab_3, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "OSSAT Platform Computer Comms"))
        self.groupBox.setTitle(_translate("Form", "Telemetry"))
        self.lblTelecommandN.setText(_translate("Form", "TC #"))
        self.pushButton.setText(_translate("Form", "Send TC REQ"))
        self.groupBox_2.setTitle(_translate("Form", "Time Commands"))
        self.pushButton_2.setText(_translate("Form", "Send PC Time"))
        self.pushButton_3.setText(_translate("Form", "Send this Time :"))
        self.dateTimeEdit.setDisplayFormat(_translate("Form", "HH:mm:ss.zzz"))
        self.groupBox_3.setTitle(_translate("Form", "Last Response"))
        self.label_3.setText(_translate("Form", "TC #"))
        self.label_4.setText(_translate("Form", "N"))
        self.label_7.setText(_translate("Form", "TIMEOUTS :"))
        self.label_8.setText(_translate("Form", "N/A"))
        self.label_5.setText(_translate("Form", "Response"))
        self.label_6.setText(_translate("Form", "N/A"))
        self.checkBox.setText(_translate("Form", "Continuous?"))
        self.lblTelecommandData.setText(_translate("Form", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "TELEMETRY"))
        self.groupBox_4.setTitle(_translate("Form", "Telecommanding"))
        self.label_2.setText(_translate("Form", "TLM CH #"))
        self.label_9.setText(_translate("Form", "N/A"))
        self.groupBox_6.setTitle(_translate("Form", "Last Response"))
        self.label.setText(_translate("Form", "Channel #"))
        self.pushButton_5.setText(_translate("Form", "Send TLM REQ"))
        self.label_13.setText(_translate("Form", "TIMEOUTS:"))
        self.label_14.setText(_translate("Form", "N/A"))
        self.checkBox_3.setText(_translate("Form", "Continuous?"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTelecommanding), _translate("Form", "TELECOMMANDING"))
        self.groupBox_5.setTitle(_translate("Form", "To Upload"))
        self.lblTelecommandData_2.setText(_translate("Form", "Upload from:"))
        self.pushButton_4.setText(_translate("Form", "Send TC REQ"))
        self.lblTelecommandN_2.setText(_translate("Form", "Upload to:"))
        self.groupBox_7.setTitle(_translate("Form", "Time Commands"))
        self.pushButton_6.setText(_translate("Form", "Send PC Time"))
        self.pushButton_7.setText(_translate("Form", "Send this Time :"))
        self.dateTimeEdit_2.setDisplayFormat(_translate("Form", "HH:mm:ss.zzz"))
        self.groupBox_8.setTitle(_translate("Form", "Last Response"))
        self.label_10.setText(_translate("Form", "TC #"))
        self.label_11.setText(_translate("Form", "N"))
        self.label_12.setText(_translate("Form", "TIMEOUTS :"))
        self.label_15.setText(_translate("Form", "N/A"))
        self.label_16.setText(_translate("Form", "Response"))
        self.label_17.setText(_translate("Form", "N/A"))
        self.pushButton_8.setText(_translate("Form", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("Form", "FILE TRANSFER"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "LOG"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "CONFIG"))
