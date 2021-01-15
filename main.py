################################################################################### 
# @file main.py 
###################################################################################
#   _  _____ ____  ____  _____
#  | |/ /_ _/ ___||  _ \| ____|
#  | ' / | |\___ \| |_) |  _|
#  | . \ | |___ ) |  __/| |___
#  |_|\_\___|____/|_|   |_____|
###################################################################################
# Copyright (c) 2020 KISPE Space Systems Ltd.
#
# Please follow the following link for the license agreement for this code:
# www.kispe.co.uk/projectlicenses/RA2001001003
###################################################################################
#  Created on: 17-Aug-2020 
#  Main app entry point 
#  @author: Ricardo Mota (ricardoflmota@gmail.com), Dennis Lien (dennis.lien.o@gmail.com)
###################################################################################

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtCore import Qt

from platform_comms_app import Ui_Form

class MainWindow(QWidget, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Should do that for all UI items, need to do this in QT designer.
        self.pushButtonSendPcTime.clicked.connect(self.onSendPcTime)
        self.pushButtonSendThisTime.clicked.connect(self.onClickThisTime)
        self.pushButtonSendTCReq.clicked.connect(self.onClickSendTCReq)

    # TODO: I think there is a better way to handle events
    # There is event handlers and signals, not sure what to use.
    # https://www.learnpyqt.com/tutorials/signals-slots-events/
    def onSendPcTime(self, event):
        # TODO: get pc time and send it.
        print('Clicked: Send PC Time')
    
    def onClickThisTime(self, event):
        # Just a test so see how we can get data from other UI items.
        timeFromUI = self.dateTimeEditSendThisTime.dateTime()
        timeString = timeFromUI.toString(self.dateTimeEditSendThisTime.displayFormat())
        print('Clicked: Send This Time')
        print(timeString)

    def onClickSendTCReq(self, event):
        tc = self.inputTelecommandN.text()
        data = self.inputTelecommandData.text()
        # Text value of the comboBox. see: https://doc.qt.io/qt-5/qcombobox.html#currentData-prop
        comboBox = self.comboBoxTelemetry.currentText()

        # It returns 2 for true, and 0 for false. Is this normal in py? 0/1 is what i would expect.
        isContinuous = self.checkBoxTelemetryContinuous.checkState() == 2

        print('TC: {}'.format(tc))
        print('Data: {}'.format(data))
        print('ComboBox: {}'.format(comboBox))
        print('Is continuous: {}'.format(isContinuous))

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
