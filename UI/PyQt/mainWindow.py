from datetime import date, datetime
import locale
import sys
from PyQt5.uic import loadUi
from PyQt5 import  QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QFormLayout
from DataProcessors import XMLProcessor as XML
import Checkbook as CB
import CheckbookTransaction as CBT
import ConfigurationProcessor as Conf
from QtCommandProcessor import QtCommandProcessor
from UI.PyQt.CopyDialog import CopyDialog
from UI.PyQt.ListTrans import ListTrans
from UI.PyQt.SingleInput import SingleInput
from UI.PyQt.TransactionDialog import TransactionDialog



conf = Conf.ConfigurationProcessor()

class MainWindow(QMainWindow):
    def __init__(self, save_function=None, load_function=None, checkbook=None):
        super(MainWindow, self).__init__()

        # need to load the checkbook to get the number of rows to add to the table
        if save_function is None:
            self.save_function = XML.XMLProcessor.save
        else:
            self.save_function = save_function
        if load_function is None:
            self.load_function = XML.XMLProcessor.load
        else:
            self.load_function = load_function

        self.checkbook = CB.Checkbook()
        if checkbook is not None:
            self.checkbook = checkbook
        else:
            self.checkbook.load("Test/test.xml", self.load_function) # Test/test.xml /home/amkirby/Sync/Registers/2023.xml



        self.command_processor = QtCommandProcessor(self.checkbook, self)

        ##########################
        # Other Windows
        ##########################
        self.single_input = SingleInput("")
        # self.display_trans = ListTrans()

        self.pyqt5_designer_setup()



        # ##########################
        # Button Config
        # ##########################
        self.add_button.clicked.connect(lambda : self.command_processor.process_add_command())
        self.save_button.clicked.connect(lambda : self.command_processor.process_save_command(self.save_function))
        self.resequence_button.clicked.connect(lambda : self.command_processor.process_resequence_command(self.checkbook))
        self.delete_button.clicked.connect(lambda : self.command_processor.process_delete_command())
        self.edit_button.clicked.connect(lambda : self.command_processor.process_edit_command())
        self.load_button.clicked.connect(lambda : self.command_processor.process_load_command(self.load_function))
        self.copy_button.clicked.connect(lambda : self.command_processor.process_copy_command("",""))
        self.quit_button.clicked.connect(self.close)

    def pyqt5_designer_setup(self):
        loadUi("UI/PyQt/mainWindow.ui", self)

        # set the column widths based around the specified sizes
        for i in range(len(conf.get_property("SIZE_LIST"))):
            self.Register_Table.setColumnWidth(i, (conf.get_property("SIZE_LIST")[i] * 7))

        # display processor methods would handle setting fields, calling window creations / creating windows,
        # and sending data back-and-forth.

        # update category dropdown dynamically based on the transaction selected
        self.Add_Trans.currentIndexChanged.connect(self.update_category)

        self.repaint()

    def update_category(self):
        trans_needed = self.Add_Trans.currentText()
        if trans_needed != "":
            trans_needed = trans_needed.upper() + "_"

        # populate the category box based on the transaction chosen
        cats = conf.get_property(trans_needed + "CATEGORIES")
        self.Add_Category.clear()
        self.Add_Category.addItems(cats)
        self.Add_Category.setCurrentIndex(0)

    def edit_command(self, data=None):
        form_layout = QFormLayout()



    def repaint(self):
        # load the checkbook data into the table
        self._load_checkbook_into_table(self.Register_Table, self.checkbook)
        
        # word wrapping
        self.Register_Table.resizeRowsToContents()

        self.Total_Value.setText(locale.currency(self.checkbook.get_total(), grouping=conf.get_property("THOUSAND_SEP")))
        
        #clear add row
        self._clear_add_row()
        self.Add_Date.setFocus()


    def display_message(self, message):
        QMessageBox.information(self, "Info", message)


    def handle_single_input(self, input_message):
        self.single_input.set_text(input_message)
        self.single_input.exec()
        return self.single_input.input_line.text()
    

    def print_list_of_trans(self, header_text, width, fill_char, list_of_trans):
        display_trans = ListTrans(list_of_trans)
        display_trans.setWindowTitle(header_text)
        display_trans.exec()

    
    def transaction_dialog(self, cbt):
        trans_dialog = TransactionDialog(cbt, self.command_processor)
        trans_dialog.setWindowTitle("Transaction")
        return_val = trans_dialog.exec()
        return return_val

    def copy_dialog(self):
        copy_dialog = CopyDialog(self.checkbook.get_file_name(), conf.get_property("DEFAULT_COPY_TO"))
        return_val = copy_dialog.exec()
        return return_val

    
    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Quit',
                "Are you sure to quit?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.command_processor.process_quit_command(self.save_function)
            event.accept()
        else:
            event.ignore()        


    def _clear_add_row(self):
        # populate the date with today's date
        add_widgets = (self.Add_CheckbookTransaction_Layout.itemAt(i).widget() for i in range(self.Add_CheckbookTransaction_Layout.count()))
        for current_widget in add_widgets:
            current_widget.clear()

        self.Add_Date.setDate(QDate.currentDate())

        # populate the category box
        cats = conf.get_property("CATEGORIES")
        self.Add_Category.addItems(cats)
        self.Add_Category.setCurrentIndex(0)

        # populate the transaction box
        trans = ["Debit", "Credit"]
        self.Add_Trans.addItems(trans)
        self.Add_Trans.setCurrentIndex(0)

        # populate the User box
        users = conf.get_property("USERS")
        self.Add_User.addItems(users)
        self.Add_User.setCurrentIndex(0)

        # set the Num field to the latest UID
        self.Add_Num.setText(str(CBT.CheckbookTransaction._uid))


    def _format(self, value):
        formatted_value = str(value)
        if type(value) is date:
            formatted_value = datetime.strftime(datetime.combine(value, datetime.min.time()), conf.get_property("DATE_FORMAT"))
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()