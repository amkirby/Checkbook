from datetime import date, datetime
import locale
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets

import CheckbookTransaction as CBT
import Checkbook as CB
import ConfigurationProcessor as Conf

conf = Conf.ConfigurationProcessor()


class ListTrans(QDialog):
    def __init__(self, list_of_trans):
        super(ListTrans, self).__init__()
        loadUi("UI/display_trans.ui", self)

        self.list_of_trans = list_of_trans
        cb = CB.Checkbook()
        cb.create_based_on_list(list_of_trans)
        self._load_checkbook_into_table(self.Register_Table, cb)


    def _format(self, value):
        formatted_value = str(value)
        if type(value) is date:
            formatted_value = datetime.strftime(value, conf.get_property("DATE_FORMAT"))
        elif type(value) is float:
            formatted_value = locale.currency(value, grouping=conf.get_property("THOUSAND_SEP"))

        

        return formatted_value

    def _load_checkbook_into_table(self,register_table, checkbook):
        row = 0
        register_table.setRowCount(len(checkbook.get_register()))
        for cbt in checkbook.get_register():
            for i in range(len(CBT.KEYS)):
                currentItem = QtWidgets.QTableWidgetItem(self._format(cbt.get_dictionary()[CBT.KEYS[i]]))
                register_table.setItem(row, i, currentItem)
                # forces a scroll to the bottom
                register_table.scrollToItem(currentItem,QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
            row += 1
