import sys
from typing import Callable, List
import CheckbookTransaction as CBT
from PyQt5.QtWidgets import QApplication

from UI.PyQt.mainWindow import MainWindow


class QtDisplayProcessor:

    def __init__(self, save_function: Callable[[str, List[CBT.CheckbookTransaction]], None], load_function: Callable[[str], List[CBT.CheckbookTransaction]], cb=None):
        # self.command_processor = command_processor # should already have the display_processor in it and shouldn't be needed here like it is for the CLI
        # self.display_processor = display_processor # instead of importing the window, pass it in as the display_processor
        self.app = QApplication(sys.argv)
        self.mainWindow = MainWindow(save_function, load_function, cb)


    def main(self):
        self.mainWindow.show()
        self.app.exec_()

