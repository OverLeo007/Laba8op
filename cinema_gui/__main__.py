from terminal_gui import *
from PyQt5.QtWidgets import QApplication

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TerminalUser()
    ex.show()
    app.exec_()
    exit()
