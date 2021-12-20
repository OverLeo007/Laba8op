import sys

from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5 import QtGui

import Cinema.cinema_interaction
from terminal_picker_gui import Ui_terminal_picker
from user_terminal_gui import Ui_UserTerminal
from admin_terminal_gui import Ui_AdminTerminal
from Cinema.terminals import UserTerminal, AdminTerminal
from Cinema.sessions_generator import generate_session


class TerminalPick(QDialog, Ui_terminal_picker):
    def __init__(self):
        super().__init__()

        with open('stylesheet_template_terminal_choicer.qss', 'r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())

        self.setupUi(self)
        self.user_terminal_button.clicked.connect(self.user_picked)
        self.admin_terminal_button.clicked.connect(self.admin_picked)

        self.user_term = TerminalUser()
        self.admin_term = TerminalAdmin()

    def user_picked(self):
        self.hide()
        self.user_term.show()

    def admin_picked(self):
        self.hide()
        self.admin_term.show()


def hider(*to_hide):
    for obj in to_hide:
        obj.hide()


def shower(*to_show):
    for obj in to_show:
        obj.show()


def cleaner(*to_clear):
    for obj in to_clear:
        obj.clear()


class TerminalUser(QWidget, Ui_UserTerminal):
    def __init__(self):
        super().__init__()

        with open('stylesheet_template_terminal_choicer.qss', 'r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())
        self.terminal = UserTerminal([generate_session(fill=True) for _ in range(10)])
        self.setupUi(self)

        self.sessionEdit.setValidator(QtGui.QIntValidator())
        self.placeEdit.setValidator(QtGui.QIntValidator())

        hider(self.buyButton, self.placeEdit, self.placeLabel, self.yesButton, self.noButton, self.nextIterLabel)

        self.toBuyButton.clicked.connect(self.buy_ticket_event)
        self.buyButton.clicked.connect(self.get_ticket)
        self.yesButton.clicked.connect(self.reset)
        self.noButton.clicked.connect(exit)

        self.make_content()

    def make_content(self):
        self.sessionsTextBrowser.setText(self.terminal.get_pretty_sessions())

    def reset(self):
        self.make_content()
        hider(self.nextIterLabel, self.yesButton, self.noButton)
        shower(self.toBuyButton, self.sessionPickLabel, self.sessionEdit)
        self.sessionPickLabel.setText('Ввведите id сеанса на который хотите купить билет')
        self.sessionEdit.clear()
        self.placeEdit.clear()

    def buy_ticket_event(self):
        if (session_id := self.sessionEdit.text()) not in self.terminal.sessions.keys():
            self.sessionEdit.setText('Сеанса с таким id не существует')
        else:
            self.terminal.set_session(session_id)
            self.sessionsTextBrowser.setText(self.terminal.picked_session.get_places_info())
            self.sessionPickLabel.setText('Введите номер ряда')
            self.sessionEdit.clear()
            self.toBuyButton.hide()
            shower(self.buyButton, self.placeEdit, self.placeLabel)

    def get_ticket(self):
        row = int(self.sessionEdit.text())
        place = int(self.placeEdit.text())
        ticket = self.terminal.buy_ticket((row, place))
        if isinstance(ticket, Cinema.cinema_interaction.Ticket):
            self.sessionsTextBrowser.setText(ticket.__str__())
        else:
            self.sessionsTextBrowser.setText(ticket)
        hider(self.placeEdit, self.placeLabel, self.sessionEdit, self.sessionPickLabel, self.buyButton)
        shower(self.nextIterLabel, self.yesButton, self.noButton)


class TerminalAdmin(QWidget, Ui_AdminTerminal):
    def __init__(self):
        super().__init__()

        with open('stylesheet_template_terminal_choicer.qss', 'r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())
        self.terminal = AdminTerminal([generate_session(fill=True) for _ in range(10)])
        self.setupUi(self)

        self.to_hide = None
        self.to_show = None
        self.to_clear = [self.filmNameLine, self.session2StatIdLine,
                         self.session2DelIdLine, self.sessionTimeLine,
                         self.ticketCostLine, self.hallTypeLine]

        self.ticketCostLine.setValidator(QtGui.QIntValidator())
        self.session2DelIdLine.setValidator(QtGui.QIntValidator())
        self.session2StatIdLine.setValidator(QtGui.QIntValidator())

        hider(self.addSessionButtion, self.filmNameLine,
              self.filmNameLabel, self.hallTypeLine,
              self.hallTypeLabel, self.sessionTimeLine,
              self.sessionTimeLabel, self.ticketCostLine,
              self.ticketCostLabel, self.delSessionLabel,
              self.delSessionButton, self.session2DelIdLine,
              self.getStatLabel, self.getStatButton,
              self.session2StatIdLine, self.backToSessionsButton)

        self.getStatEventButton.clicked.connect(self.get_statistics_event)
        self.getStatButton.clicked.connect(self.get_statistics)
        self.delSessionEventButton.clicked.connect(self.delete_session_event)
        self.delSessionButton.clicked.connect(self.delete_session)
        self.addSessionEventButton.clicked.connect(self.add_session_event)
        self.addSessionButtion.clicked.connect(self.add_session)
        self.backToSessionsButton.clicked.connect(self.reset)

        self.make_content()

    def make_content(self):
        self.sessionsTextBrowser.setText(self.terminal.get_pretty_sessions())

    def reset(self):
        self.make_content()
        hider(*self.to_show)
        shower(*self.to_hide)
        cleaner(*self.to_clear)

    def get_statistics_event(self):
        self.to_hide = [self.addSessionEventButton, self.delSessionEventButton,
                        self.getStatEventButton, self.tableLable]
        self.to_show = [self.getStatLabel, self.getStatButton,
                        self.session2StatIdLine, self.backToSessionsButton]
        hider(*self.to_hide)
        shower(*self.to_show)

    def get_statistics(self):
        if (session_id := self.session2StatIdLine.text()) not in self.terminal.sessions.keys():
            self.session2StatIdLine.setText('Сеанса с таким id не существует')
        else:
            self.sessionsTextBrowser.setText(self.terminal.session_pick(session_id)['session'].get_stat())

    def delete_session_event(self):
        self.to_hide = [self.addSessionEventButton, self.delSessionEventButton,
                        self.getStatEventButton, self.tableLable]
        self.to_show = [self.delSessionLabel, self.delSessionButton,
                        self.session2DelIdLine, self.backToSessionsButton]
        hider(*self.to_hide)
        shower(*self.to_show)

    def delete_session(self):
        if (session_id := self.session2DelIdLine.text()) not in self.terminal.sessions.keys():
            self.session2DelIdLine.setText('Сеанса с таким id не существует')
        else:
            self.sessionsTextBrowser.setText(f'Сеанс с id '
                                             f'{self.terminal.del_session(session_id)} '
                                             f'успешно удален')

    def add_session_event(self):
        self.to_hide = [self.addSessionEventButton, self.delSessionEventButton,
                        self.getStatEventButton, self.tableLable,
                        self.sessionsTextBrowser]
        self.to_show = [self.addSessionButtion, self.backToSessionsButton,
                        self.filmNameLabel, self.filmNameLine,
                        self.hallTypeLabel, self.hallTypeLine,
                        self.sessionTimeLabel, self.sessionTimeLine,
                        self.ticketCostLabel, self.ticketCostLine]
        hider(*self.to_hide)
        shower(*self.to_show)

    def add_session(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TerminalAdmin()
    ex.show()
    app.exec_()
    exit()
