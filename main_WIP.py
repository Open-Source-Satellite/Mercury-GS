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

        # TODO: Should rename the button names.
        # Should do that for all UI items, need to do this in QT designer.
        self.pushButton_2.clicked.connect(self.onClick)
        self.pushButton_3.clicked.connect(self.onClickThisTime)

    # TODO: I think there is a better way to handle events
    # There is event handlers and signals, not sure what to use.
    # https://www.learnpyqt.com/tutorials/signals-slots-events/
    def onClick(self, event):
        print('Clicked: Send PC Time')
    
    def onClickThisTime(self, event):
        # Just a test so see how we can get data from other UI items.
        timeFromUI = self.dateTimeEdit.dateTime()
        timeString = timeFromUI.toString(self.dateTimeEdit.displayFormat())
        print('Clicked: Send This Time')
        print(timeString)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
