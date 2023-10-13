from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate

from PyQt5.uic import loadUi

import ConfigurationProcessor as Conf

conf = Conf.ConfigurationProcessor()


class TransactionDialog(QDialog):
    def __init__(self, cbt, command_processor):
        super(TransactionDialog, self).__init__()
        loadUi("UI/PyQt/transaction.ui", self)
        self.transaction = cbt
        self.processor = command_processor

        self.create_fields()

    def create_fields(self):
        # populate the category box
        cats = conf.get_property("CATEGORIES")
        self.Category.addItems(cats)
        self.Category.setCurrentIndex(0)

        # populate the transaction box
        trans = ["Debit", "Credit"]
        self.Trans.addItems(trans)
        self.Trans.setCurrentIndex(0)

        # populate the User box
        users = conf.get_property("USERS")
        self.User.addItems(users)
        self.User.setCurrentIndex(0)

        # populate values from the transaction
        self.Date.setDate(QDate(self.transaction.get_date()))
        self.User.setCurrentText(self.transaction.get_value("User"))
        self.Trans.setCurrentText(self.transaction.get_value("Trans"))
        self.Category.setCurrentText(self.transaction.get_value("Category"))
        self.Desc.setText(self.transaction.get_value("Desc"))
        self.Amount.setText(str(self.transaction.get_value("Amount")))
        self.Num.setText(self.transaction.get_value("Num"))

    def accept(self) -> None:
        # save the transaction
        self.transaction.set_value("Date", self.Date.date().toPyDate().__format__(conf.get_property("DATE_FORMAT")))
        self.transaction.set_value("User", self.User.currentText())
        self.transaction.set_value("Trans", self.Trans.currentText())
        self.transaction.set_value("Category", self.Category.currentText())
        self.transaction.set_value("Desc", self.Desc.text())
        self.transaction.set_value("Amount", float(self.Amount.text()))
        self.processor._apply_debit_multiplier(self.transaction)
        super().accept()
