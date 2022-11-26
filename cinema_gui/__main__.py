from terminal_gui import TerminalPick
from PyQt5.QtWidgets import QApplication

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TerminalPick()
    ex.show()
    app.exec_()
    exit()
