import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import *

from PyQt5.uic import loadUi

import ConfigurationProcessor as Conf

conf = Conf.ConfigurationProcessor()


class CopyDialog(QDialog):
    def __init__(self, from_file, to_file):
        super(CopyDialog, self).__init__()
        loadUi("UI/copy_input.ui", self)
        self.from_file = from_file
        self.to_file = to_file

        self.from_file_input.setPlaceholderText(self.from_file)
        self.to_file_input.setPlaceholderText(self.to_file)

    
    def accept(self) -> None:
        # if input is blank, use placeholder
        # if input has value, use the value
        return super().accept()

