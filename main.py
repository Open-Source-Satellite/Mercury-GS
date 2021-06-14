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
        # self.pushButtonSendPcTime.clicked.connect(self.on_send_pc_time)
        # self.pushButtonSendThisTime.clicked.connect(self.on_click_this_time)
        # self.pushButtonSendTCReq.clicked.connect(self.onClickSendTCReq) AUTOCONNECTED
        # self.pushButtonSendTlmReq.clicked.connect(self.onClickSendTLMReq) AUTOCONNECTED
        # self.pushButtonOpenFileUploadFrom.clicked.connect(self.on_click_upload_open)
        # self.pushButtonOpenFileDownloadTo.clicked.connect(self.on_click_download_open)
        # self.comboBoxCommsBaudValue.currentTextChanged.connect(self.on_baud_rate_change)

        # Init UART
        from low_level.serial_comms import serial_comms_init
        serial_comms_init()
        # Register all callbacks
        from telemetry import telemetry_register_callback
        from telecommand import telecommand_register_callback
        from low_level.packet import packet_register_callback, packet_init
        telemetry_register_callback(self.telemetry_response_receive)
        telecommand_register_callback(self.telecommand_response_receive)
        packet_register_callback(telemetry.tlm_response, telecommand.tc_response)
        packet_init()
        # Set COMMS Baud Rate
        config.BAUD_RATE = self.comboBoxCommsBaudValue.currentText()
        # Set TC_TLM Rate
        config.TC_TLM_RATE = self.spinBoxTcTlmRateValue.value()

    # TODO: I think there is a better way to handle events
    # There is event handlers and signals, not sure what to use.
    # https://www.learnpyqt.com/tutorials/signals-slots-events/
    def on_send_pc_time(self, event):
        # TODO: get pc time and send it.
        print('Clicked: Send PC Time')

    def on_click_this_time(self, event):
        date_from_ui = self.dateEditSendThisTime.dateTime()
        date_string = date_from_ui.toString(self.dateEditSendThisTime.displayFormat())

        time_from_ui = self.dateTimeEditSendThisTime.dateTime()
        time_string = time_from_ui.toString(self.dateTimeEditSendThisTime.displayFormat())

        print('Clicked: Send This Time')
        print('Date: {}'.format(date_string))
        print('Time: {}'.format(time_string))

    def on_click_send_telecommand_request(self, event):
        tc = self.spinBoxTcNumberValue.value()
        data = self.inputTcData.text()
        # Text value of the comboBox. see: https://doc.qt.io/qt-5/qcombobox.html#currentData-prop
        datatype = self.comboBoxTcDataType.currentText()

        # It returns 2 for true, and 0 for false. Is this normal in py? 0/1 is what i would expect.
        is_continuous = self.checkBoxTcReqContinuous.checkState() == 2

        print('TC: {}'.format(tc))
        print('Data: {}'.format(data))
        print('DataType: {}'.format(datatype))
        print('Is continuous: {}'.format(is_continuous))

        telecommand.tc_request_send(tc, data, datatype)

    def on_click_send_telemetry_request(self, event):
        # labelTimeOuts
        tlm_channel = self.spinBoxTlmAdHocChValue.value()
        is_continuous = self.checkBoxTlmReqContinuous.checkState() == 2

        # Set the TIMEOUTS value here;
        self.labelTlmTimeoutValue.setText('0')

        print('Channel: {}'.format(tlm_channel))
        print('Is continuous: {}'.format(is_continuous))

        telemetry.tlm_request_send(tlm_channel, is_continuous)

    def on_click_upload_open(self, event):
        file_dialog = QFileDialog(self)
        file_dialog.show()

        file_path = file_dialog.getOpenFileName()[0]
        file_dialog.hide()

        self.lineEditUploadFrom.setText(file_path)

    def on_click_upload_abort(self, event):
        pass

    def on_click_download_open(self, event):
        file_dialog = QFileDialog(self)
        file_dialog.show()

        file_path = file_dialog.getOpenFileName()[0]
        file_dialog.hide()

        self.lineEditDownloadTo.setText(file_path)

    def on_baud_rate_change(self, event):
        config.BAUD_RATE = self.comboBoxCommsBaudValue.currentText()

    def on_tc_tlm_rate_change(self, event):
        config.TC_TLM_RATE = self.spinBoxTcTlmRateValue.value()

    def telemetry_response_receive(self, telemetry_channel, telemetry_data):
        if telemetry_channel == 1:
            self.labelTlmChOneValue.setText(telemetry_data)
        elif telemetry_channel == 2:
            self.labelTlmChTwoValue.setText(telemetry_data)
        elif telemetry_channel == 3:
            self.labelTlmChThreeValue.setText(telemetry_data)

    def telecommand_response_receive(self, telecommand_number, telecommand_data):
        self.labelTelecommandResNumberValue.setText(telecommand_number)
        self.labelTelecommandResStatus.setText(telecommand_data)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
