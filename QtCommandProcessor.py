
import string
import Checkbook as CB
from Tools import copyToAnother as CTA
from CommandProcessor import CommandProcessor
import CheckbookTransaction as CBT
from PyQt5.QtWidgets import QComboBox, QTextEdit, QMessageBox


class QtCommandProcessor(CommandProcessor):
    def __init__(self, checkbook, main_window):
        #display_processor is the MainWindow
        super().__init__(checkbook, main_window)
        self.main_window = main_window

    def _get_text_from_widget(self, widget):
        text = ""
        if isinstance(widget, QComboBox):
            text = widget.currentText()
        elif isinstance(widget, QTextEdit):
            text = string.capwords(widget.toPlainText())
        else:
            text = widget.text()

        return text

    def confirm_selection(self, selection):
        is_confirmed = False
        select = QMessageBox.question(self.main_window, 'Confirmation...',
                "Do you want to " + selection + "?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No) # to become confirm selection
        
        if select == QMessageBox.Yes:
            is_confirmed = True

        return is_confirmed

    def process_resequence_command(self, checkbook) -> None:
        super().process_resequence_command(checkbook)
        self.main_window.repaint()
        
    
    def process_delete_command(self, *args: str) -> None:
        super().process_delete_command(*args)
        self.main_window.repaint()

    def process_load_command(self, load_function, *args) -> None:
        super().process_load_command(load_function, *args)
        self.main_window.repaint()
    
    def process_edit_command(self, *args: str) -> None:
        transactions_to_edit = self._process_list_input(self.display_processor.handle_single_input("Which transaction(s) do you want to edit? : "))

        transactions_from_cb = self.checkbook.find_transactions(transactions_to_edit)

        self.display_processor.print_list_of_trans(" Transaction(s) Being Edited ", self.conf.get_property("MAX_WIDTH"), self.conf.get_property("TRANS_FILL_CHAR"), transactions_from_cb)
        if(transactions_from_cb and self.confirm_selection("edit")):
            for trans in transactions_from_cb:
                exit_status = self.main_window.transaction_dialog(trans)
                if exit_status:
                    self.checkbook.set_edited(True)


        self.main_window.repaint()


    def process_copy_command(self, from_file: str, to_file: str) -> None:
        # super().process_copy_command(from_file, to_file)
        # get back the from and to files adn then do the processing here
        self.main_window.copy_dialog()
        # CTA.qt_copy(from_file, to_file)
    

    def process_print_command(self, checkbook, *args):
        return super().process_print_command(checkbook, *args)
        
    
    def process_add_command(self) -> None:
        cbt = CBT.CheckbookTransaction()
        val = ""
        add_widgets = (self.main_window.Add_CheckbookTransaction_Layout.itemAt(i).widget() for i in range(self.main_window.Add_CheckbookTransaction_Layout.count()))
        key_val = 0
        try:
            for current_widget in add_widgets:
                val = self._get_text_from_widget(current_widget)
                cbt.set_value(CBT.KEYS[key_val], val)

                key_val += 1
        except ValueError as e:
            CBT.CheckbookTransaction.decrement_uid()
            self.main_window.repaint()
            if "time data" in repr(e):
                QMessageBox.critical(self.main_window, "Error", "Invalid date entered of: " + val)
            elif "convert string to float" in repr(e):
                QMessageBox.critical(self.main_window, "Error", "Invalid amount entered of: " + val)
            else:
                QMessageBox.critical(self.main_window, "Error", str(e))

        
        self._apply_debit_multiplier(cbt)
        self.checkbook.add_single_trans(cbt)
        self.main_window.repaint()
