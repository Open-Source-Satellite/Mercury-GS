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

from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget

import telemetry
import telecommand
import config
from platform_comms_app import Ui_Form


class MainWindow(QWidget, Ui_Form):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Should do that for all UI items, need to do this in QT designer.
        self.pushButtonSendPcTime.clicked.connect(self.onSendPcTime)
        self.pushButtonSendThisTime.clicked.connect(self.onClickThisTime)
        self.pushButtonSendTCReq.clicked.connect(self.onClickSendTCReq)
        self.pushButtonSendTlmReq.clicked.connect(self.onClickSendTLMReq)

        self.pushButtonOpenFileUploadFrom.clicked.connect(self.onClickUploadOpen)
        self.pushButtonOpenFileDownloadTo.clicked.connect(self.onClickDownloadOpen)
        self.comboBoxCommsBaud.currentTextChanged.connect(self.onBaudRateChange)

        # Init UART
        import low_level
        low_level.init()
        # Register all callbacks
        from telemetry import telemetry_register_callback
        from telecommand import telecommand_register_callback
        from packet import packet_register_callback, packet_init
        telemetry_register_callback(self.telemetryReceive)
        telecommand_register_callback(self.telecommandReceive)
        packet_register_callback(telemetry.tlm_response, telecommand.tc_response)
        packet_init()
        # Set COMMS Baud Rate
        config.BAUD_RATE = self.comboBoxCommsBaud.currentText()

    # TODO: I think there is a better way to handle events
    # There is event handlers and signals, not sure what to use.
    # https://www.learnpyqt.com/tutorials/signals-slots-events/
    def onSendPcTime(self, event):
        # TODO: get pc time and send it.
        print('Clicked: Send PC Time')

    def onClickThisTime(self, event):
        dateFromUi = self.dateEditSendThisTime.dateTime()
        dateString = dateFromUi.toString(self.dateEditSendThisTime.displayFormat())

        timeFromUI = self.dateTimeEditSendThisTime.dateTime()
        timeString = timeFromUI.toString(self.dateTimeEditSendThisTime.displayFormat())

        print('Clicked: Send This Time')
        print('Date: {}'.format(dateString))
        print('Time: {}'.format(timeString))

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

        telecommand.tc_request_send(tc, data, )

    def onClickSendTLMReq(self, event):
        # labelTimeOuts
        tlmChannel = self.lineEditChannel.text()
        isContinuous = self.checkBoxLastReqContinuous.checkState() == 2

        # Set the TIMEOUTS value here;
        self.labelTLMTimeouts.setText('0')

        print('Channel: {}'.format(tlmChannel))
        print('Is continuous: {}'.format(isContinuous))

        telemetry.tlm_request_send(tlmChannel, isContinuous)


    def onClickUploadOpen(self, event):
        fileDialog = QFileDialog(self)
        fileDialog.show()

        filePath = fileDialog.getOpenFileName()[0]
        fileDialog.hide()

        self.lineEditUploadFrom.setText(filePath)

    def onClickDownloadOpen(self, event):
        fileDialog = QFileDialog(self)
        fileDialog.show()

        filePath = fileDialog.getOpenFileName()[0]
        fileDialog.hide()

        self.lineEditDownloadTo.setText(filePath)

    def onBaudRateChange(self, event):
        config.BAUD_RATE = self.comboBoxCommsBaud.currentText()

    def telemetryReceive(self, telemetry_channel, telemetry_data):
        if telemetry_channel == 1:
            self.labelTlmChOneValue.setText(telemetry_data)
        elif telemetry_channel == 2:
            self.labelTlmChTwoValue.setText(telemetry_data)
        elif telemetry_channel == 3:
            self.labelTlmChThreeValue.setText(telemetry_data)

    def telecommandReceive(self, telecommand_data):
        pass


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
