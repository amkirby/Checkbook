from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi




class SingleInput(QDialog):
    def __init__(self, input_message):
        super(SingleInput, self).__init__()
        loadUi("UI/PyQt/single_input.ui", self)
        self.input_message = input_message
        self.input_label.setText(input_message)

    def show(self) -> None:
        self.input_label.setText("")
        super().show()


    def exec(self) -> int:
        self.input_line.setFocus()
        self.input_line.setText("")
        return super().exec()


    def set_text(self, input_message):
        self.input_message = input_message
        self.input_label.setText(input_message)
