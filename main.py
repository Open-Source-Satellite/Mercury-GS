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
from PyQt5.QtWidgets import QApplication, QFileDialog, QApplication, QMainWindow, QErrorMessage
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtCore import QRegExp, QFile
import low_level.continuous
import telemetry
import telecommand
import config
import test
import sys
from platform_comms_app import Ui_MainWindow

UINT_MAX = 4294967295
UINT_MIN = 0
S64INT_MAX = 9223372036854775807
S64INT_MIN = -9223372036854775808


# Validator for unsigned 32 bit integer
class UIntValidator(QValidator):
    def __init__(self, parent):
        QValidator.__init__(self, parent)

    def validate(self, s, pos):
        try:
            if s == "":
                # Backspace or delete
                return QValidator.Acceptable, s, pos
            if int(s) > UINT_MAX or int(s) < UINT_MIN:
                return QValidator.Invalid, s, pos
        except ValueError:
            return QValidator.Invalid, s, pos

        return QValidator.Acceptable, s, pos


# Validator for signed 64 bit integer
class SixtyFourBitIntValidator(QValidator):
    def __init__(self, parent):
        QValidator.__init__(self, parent)

    def validate(self, s, pos):
        try:
            if s == "" or s == "-":
                # Backspace or delete or minus
                return QValidator.Acceptable, s, pos
            if int(s) > S64INT_MAX or int(s) < S64INT_MIN:
                return QValidator.Invalid, s, pos
        except ValueError:
            return QValidator.Invalid, s, pos

        return QValidator.Acceptable, s, pos


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Set validators for GUI elements
        self.inputTcTlmRateValue.setValidator(QIntValidator(0, 1000, self.inputTcTlmRateValue))
        self.inputTcNumberValue.setValidator(UIntValidator(self.inputTcNumberValue))
        self.inputTcTlmTimeoutValue.setValidator(QIntValidator(0, 1000, self.inputTcTlmTimeoutValue))
        self.inputTlmAdHocChannelValue.setValidator(UIntValidator(self.inputTlmAdHocChannelValue))
        self.inputTcDataValue.setValidator(QRegExpValidator(QRegExp("[A-Za-z]{0,8}"), self.inputTcDataValue))

        # Init Serial Comms
        from low_level.serial_comms import serial_comms_init, serial_comms_register_callback
        serial_comms_init("COM19", 9600)
        # Register all callbacks
        from telemetry import telemetry_register_callback
        from telecommand import telecommand_register_callback
        from low_level.packet import packet_register_callback, packet_init
        from test import test_register_callback
        from low_level.continuous import continuous_register_callback
        from config import config_register_callback
        telemetry_register_callback(self.telemetry_response_receive, self.telemetry_timeout, self.error_message_box)
        telecommand_register_callback(self.telecommand_response_receive, self.telecommand_timeout, self.error_message_box)
        packet_register_callback(telemetry.tlm_response, telecommand.tc_response, self.error_message_box)
        test_register_callback(self.test_response_receive, self.error_message_box)
        serial_comms_register_callback(self.error_message_box)
        continuous_register_callback(self.error_message_box)
        config_register_callback(self.error_message_box)
        packet_init()

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
        tc = self.inputTcNumberValue.text()
        data = self.inputTcDataValue.text()
        # Text value of the comboBox. see: https://doc.qt.io/qt-5/qcombobox.html#currentData-prop
        datatype = self.comboBoxTcDataType.currentText()

        # It returns 2 for true, and 0 for false. Is this normal in py? 0/1 is what i would expect.
        is_continuous = self.checkBoxTcReqContinuous.checkState() == 2

        print('TC: {}'.format(tc))
        print('Data: {}'.format(data))
        print('DataType: {}'.format(datatype))
        print('Is continuous: {}'.format(is_continuous))

        telecommand.tc_request_send(tc, data, datatype, is_continuous)

    def on_click_send_telemetry_request(self, event):
        tlm_channel = self.inputTlmAdHocChannelValue.text()
        is_continuous = self.checkBoxTlmReqContinuous.checkState() == 2

        print('Channel: {}'.format(tlm_channel))
        print('Is continuous: {}'.format(is_continuous))

        telemetry.tlm_request_send(tlm_channel, is_continuous)

    def on_click_test_transmit(self):
        delimiter = self.inputDelimiter.text()
        reserved_bytes = [self.inputReservedBytes1.text(), self.inputReservedBytes2.text(), self.inputReservedBytes3.text()]
        data_type = self.inputDataType.text()
        data_length = self.inputDataLength.text()
        data_field = self.inputDataField.text()

        test.transmit_test_frame(delimiter, reserved_bytes, data_type, data_length, data_field)

    def test_response_receive(self, test_response):
        self.outputResponse.setText(test_response)

    def on_click_upload_open(self, event):
        file_dialog = QFileDialog(self)
        file_dialog.show()

        file_path = file_dialog.getOpenFileName()[0]
        file_dialog.hide()

        self.inputUploadFrom.setText(file_path)

    def on_click_upload_abort(self, event):
        pass

    def on_click_download_open(self):
        file_dialog = QFileDialog(self)
        file_dialog.show()

        file_path = file_dialog.getOpenFileName()[0]
        file_dialog.hide()

        self.inputDownloadTo.setText(file_path)

    def on_baud_rate_change(self):
        from low_level.serial_comms import change_baud_rate
        change_baud_rate(int(self.comboBoxCommsBaudValue.currentText()))

    def on_tc_tlm_rate_change(self):
        rate_change = self.inputTcTlmRateValue.text()
        if rate_change != "" and rate_change != "0":
            low_level.continuous.adjust_continuous(int(rate_change))
        else:
            self.error_message_box("ERROR: Invalid Rate Value")
            low_level.continuous.continuous_stop()

    def on_timeout_change(self):
        timeout_change = self.inputTcTlmTimeoutValue.text()
        if timeout_change != "" or timeout_change != 0:
            config.change_timeout(timeout_change)
        else:
            self.error_message_box("ERROR: Invalid Timeout Value")

    def on_com_port_change(self):
        from low_level.serial_comms import change_com_port
        config.COM_PORT = self.inputComPort.currentText()
        change_com_port(config.COM_PORT)

    def on_continuous_toggle(self, is_continuous):
        if is_continuous is False:
            low_level.continuous.continuous_stop()

    def on_select_tc_datatype(self):
        self.inputTcDataValue.setValidator(None)
        self.inputTcDataValue.clear()
        if self.comboBoxTcDataType.currentText() == "String":
            self.inputTcDataValue.setValidator(QRegExpValidator(QRegExp("[A-Za-z]{0,8}"), self.inputTcDataValue))
        elif self.comboBoxTcDataType.currentText() == "Integer":
            self.inputTcDataValue.setValidator(SixtyFourBitIntValidator(self.inputTcDataValue))
        elif self.comboBoxTcDataType.currentText() == "Floating Point":
            self.inputTcDataValue.setValidator(QDoubleValidator())

    def telemetry_response_receive(self, telemetry_channel, telemetry_data):
        if telemetry_channel == 1:
            self.labelTlmChOneValue.setText(telemetry_data)
        elif telemetry_channel == 2:
            self.labelTlmChTwoValue.setText(telemetry_data)
        elif telemetry_channel == 3:
            self.labelTlmChThreeValue.setText(telemetry_data)

    def telecommand_response_receive(self, telecommand_number, telecommand_data):
        self.labelTcResNumberValue.setText(telecommand_number)
        self.labelTcResStatus.setText(telecommand_data)

    def telemetry_timeout(self):
        timeout_count = int(self.labelTlmTimeoutsValue.text()) + 1
        self.labelTlmTimeoutsValue.setText(str(timeout_count))

    def telecommand_timeout(self):
        timeout_count = int(self.labelTcResTimeoutsValue.text()) + 1
        self.labelTcResTimeoutsValue.setText(str(timeout_count))

    def error_message_box(self, error_text, error_timeout=5000):
        self.statusbar.showMessage(error_text, error_timeout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
