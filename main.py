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
import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

import config
from config import config_register_callback, change_timeout, OS, COMMS, RaspberryPi
from low_level.continuous import continuous_register_callback, adjust_continuous, continuous_stop
from low_level.packet import packet_register_callback, packet_init
from low_level.comms import comms_init, comms_register_callback, change_baud_rate, change_com_port
from platform_comms_app import Ui_MainWindow
from telecommand import tc_request_send, telecommand_register_callback, tc_response
from telemetry import tlm_rejection_response, tlm_request_send, telemetry_register_callback, tlm_response
from test import transmit_test_frame, test_register_callback

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
        self.inputTcDataValue.setValidator(QRegExpValidator(QRegExp(".{0,8}"), self.inputTcDataValue))

        self.tlm_response_field = ({"channel": self.labelTlmSlot1, "value": self.labelTlmSlot1Value},
                                   {"channel": self.labelTlmSlot2, "value": self.labelTlmSlot2Value},
                                   {"channel": self.labelTlmSlot3, "value": self.labelTlmSlot3Value},
                                   {"channel": self.labelTlmSlot4, "value": self.labelTlmSlot4Value},
                                   {"channel": self.labelTlmSlot5, "value": self.labelTlmSlot5Value},
                                   {"channel": self.labelTlmSlot6, "value": self.labelTlmSlot6Value},
                                   {"channel": self.labelTlmSlot7, "value": self.labelTlmSlot7Value},
                                   {"channel": self.labelTlmSlot8, "value": self.labelTlmSlot8Value},
                                   {"channel": self.labelTlmSlot9, "value": self.labelTlmSlot9Value},
                                   {"channel": self.labelTlmSlot10, "value": self.labelTlmSlot10Value},
                                   {"channel": self.labelTlmSlot11, "value": self.labelTlmSlot11Value},
                                   {"channel": self.labelTlmSlot12, "value": self.labelTlmSlot12Value},
                                   {"channel": self.labelTlmSlot13, "value": self.labelTlmSlot13Value},
                                   {"channel": self.labelTlmSlot14, "value": self.labelTlmSlot14Value},
                                   {"channel": self.labelTlmSlot15, "value": self.labelTlmSlot15Value},
                                   {"channel": self.labelTlmSlot16, "value": self.labelTlmSlot16Value},
                                   {"channel": self.labelTlmSlot17, "value": self.labelTlmSlot17Value},
                                   {"channel": self.labelTlmSlot18, "value": self.labelTlmSlot18Value},
                                   {"channel": self.labelTlmSlot19, "value": self.labelTlmSlot19Value},
                                   {"channel": self.labelTlmSlot20, "value": self.labelTlmSlot20Value},
                                   {"channel": self.labelTlmSlot21, "value": self.labelTlmSlot21Value},
                                   {"channel": self.labelTlmSlot22, "value": self.labelTlmSlot22Value},
                                   {"channel": self.labelTlmSlot23, "value": self.labelTlmSlot23Value},
                                   {"channel": self.labelTlmSlot24, "value": self.labelTlmSlot24Value},
                                   {"channel": self.labelTlmSlot25, "value": self.labelTlmSlot25Value},
                                   {"channel": self.labelTlmSlot26, "value": self.labelTlmSlot26Value},
                                   {"channel": self.labelTlmSlot27, "value": self.labelTlmSlot27Value},
                                   {"channel": self.labelTlmSlot28, "value": self.labelTlmSlot28Value},
                                   {"channel": self.labelTlmSlot29, "value": self.labelTlmSlot29Value},
                                   {"channel": self.labelTlmSlot30, "value": self.labelTlmSlot30Value},
                                   {"channel": self.labelTlmSlot31, "value": self.labelTlmSlot31Value},
                                   {"channel": self.labelTlmSlot32, "value": self.labelTlmSlot32Value},
                                   {"channel": self.labelTlmSlot33, "value": self.labelTlmSlot33Value},
                                   {"channel": self.labelTlmSlot34, "value": self.labelTlmSlot34Value},
                                   {"channel": self.labelTlmSlot35, "value": self.labelTlmSlot35Value},
                                   {"channel": self.labelTlmSlot36, "value": self.labelTlmSlot36Value},
                                   {"channel": self.labelTlmSlot37, "value": self.labelTlmSlot37Value},
                                   {"channel": self.labelTlmSlot38, "value": self.labelTlmSlot38Value},
                                   {"channel": self.labelTlmSlot39, "value": self.labelTlmSlot39Value},
                                   {"channel": self.labelTlmSlot40, "value": self.labelTlmSlot40Value})

        self.tlm_response_list = list()

        for tlm_slot in self.tlm_response_field:
            tlm_slot["channel"].setText("")
            tlm_slot["value"].setText("")

        if RaspberryPi is False:
            self.comboBoxComms.setEnabled(False)

        # Init Serial Comms
        comms_init("COM1", 9600)
        # Register all callbacks
        telemetry_register_callback(self.telemetry_response_receive, self.telemetry_rejection_response_receive,
                                    self.telemetry_timeout, self.error_message_box)
        telecommand_register_callback(self.telecommand_response_receive, self.telecommand_timeout,
                                      self.error_message_box)
        packet_register_callback(tlm_response, tlm_rejection_response, tc_response, self.error_message_box)
        test_register_callback(self.test_response_receive, self.error_message_box)
        comms_register_callback(self.error_message_box)
        continuous_register_callback(self.error_message_box)
        config_register_callback(self.error_message_box)
        packet_init()

        # Disable UART config if Linux TODO: Make this compatible, tty etc as well as COM
        if OS == "Linux":
            self.comboBoxCommsBaudValue.setEnabled(False)
            self.inputComPort.setEnabled(False)

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

        tc_request_send(tc, data, datatype, is_continuous)

    def on_click_send_telemetry_request(self, event):
        tlm_channel = self.inputTlmAdHocChannelValue.text()
        is_continuous = self.checkBoxTlmReqContinuous.checkState() == 2

        print('Channel: {}'.format(tlm_channel))
        print('Is continuous: {}'.format(is_continuous))

        tlm_request_send(tlm_channel, is_continuous)

    def on_click_test_transmit(self):
        delimiter = self.inputDelimiter.text()
        reserved_bytes = [self.inputReservedBytes1.text(), self.inputReservedBytes2.text(),
                          self.inputReservedBytes3.text()]
        data_type = self.inputDataType.text()
        data_length = self.inputDataLength.text()
        data_field = self.inputDataField.text()

        transmit_test_frame(delimiter, reserved_bytes, data_type, data_length, data_field)

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
        change_baud_rate(int(self.comboBoxCommsBaudValue.currentText()))

    def on_tc_tlm_rate_change(self):
        rate_change = self.inputTcTlmRateValue.text()
        if rate_change != "" and rate_change != "0":
            adjust_continuous(int(rate_change))
        else:
            self.error_message_box("ERROR: Invalid Rate Value")
            continuous_stop()

    def on_timeout_change(self):
        timeout_change = self.inputTcTlmTimeoutValue.text()
        if timeout_change != "" or timeout_change != 0:
            change_timeout(timeout_change)
        else:
            self.error_message_box("ERROR: Invalid Timeout Value")

    def on_com_port_change(self):
        import config
        config.COM_PORT = self.inputComPort.currentText()
        change_com_port(config.COM_PORT)

    def on_comms_change(self):
        import config
        config.COMMS = self.comboBoxComms.currentText()
        if config.COMMS == "SERIAL":
            self.comboBoxCommsBaudValue.setEnabled(True)
            self.inputComPort.setEnabled(True)
        elif config.COMMS == "RF69":
            self.comboBoxCommsBaudValue.setEnabled(False)
            self.inputComPort.setEnabled(False)

    def on_continuous_toggle(self, is_continuous):
        if is_continuous is False:
            continuous_stop()

    def on_select_tc_datatype(self):
        self.inputTcDataValue.setValidator(None)
        self.inputTcDataValue.clear()
        if self.comboBoxTcDataType.currentText() == "String":
            self.inputTcDataValue.setValidator(QRegExpValidator(QRegExp(".{0,8}"), self.inputTcDataValue))
        elif self.comboBoxTcDataType.currentText() == "Integer":
            self.inputTcDataValue.setValidator(SixtyFourBitIntValidator(self.inputTcDataValue))
        elif self.comboBoxTcDataType.currentText() == "Floating Point":
            self.inputTcDataValue.setValidator(QDoubleValidator())

    def telemetry_response_receive(self, telemetry_channel, telemetry_data):

        if not any(d.get('channel') == telemetry_channel for d in self.tlm_response_list):
            self.tlm_response_list.append({"channel": telemetry_channel, "value": telemetry_data})
        else:
            for item in self.tlm_response_list:
                if item["channel"] == telemetry_channel:
                    item["value"] = telemetry_data

        from operator import itemgetter
        self.tlm_response_list = sorted(self.tlm_response_list, key=itemgetter("channel"))

        for slot, telemetry_to_plot in zip(self.tlm_response_field, self.tlm_response_list):
            slot["channel"].setText("TLM CH " + telemetry_to_plot["channel"])
            slot["value"].setText(telemetry_to_plot["value"])

    def telemetry_rejection_response_receive(self, telemetry_channel, telemetry_rejection_code):
        self.labelTlmErrChannelValue.setText(telemetry_channel)
        self.labelTlmErrReasonValue.setText(telemetry_rejection_code)

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
