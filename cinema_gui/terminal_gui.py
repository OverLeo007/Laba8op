import sys

import re
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox
from PyQt5 import QtGui

import Cinema.cinema_interaction
from terminal_picker_gui import Ui_terminal_picker
from user_terminal_gui import Ui_UserTerminal
from admin_terminal_gui import Ui_AdminTerminal
from Cinema.terminals import UserTerminal, AdminTerminal
from Cinema.sessions_generator import generate_session


def hider(*to_hide):
    """
    Функция, выполняющая скрытие объектов PyQt5, передеанных в to_hide
    :param to_hide: list, объекты для скрытия
    """
    for obj in to_hide:
        obj.hide()


def shower(*to_show):
    """
    Функция, показывающая объекты PyQt5, передеанных в to_hide
    :param to_hide: list, объекты для показа
    """
    for obj in to_show:
        obj.show()


def cleaner(*to_clear):
    """
    Функция, очищающая текст, внутри объектов PyQt5, переданных в to_clear
    :param to_clear: Объекты для очистки
    """
    for obj in to_clear:
        obj.clear()


class TerminalPick(QDialog, Ui_terminal_picker):
    """
    Класс окна, предоставляющего возможность выбрать тип терминала и узнать о программе
    """

    def __init__(self):
        super().__init__()

        with open('stylesheet_template_terminal_choicer.qss', 'r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())
        self.setupUi(self)
        with open('about.html', 'r', encoding='utf-8') as about_text:
            self.aboutTextBrowser.setText(about_text.read())

        self.user_terminal_button.clicked.connect(self.user_picked)
        self.admin_terminal_button.clicked.connect(self.admin_picked)
        self.aboutButton.clicked.connect(self.about_picked)
        self.backButton.clicked.connect(self.back_to_pick)

        hider(self.aboutTextBrowser, self.backButton)

        self.user_term = TerminalUser()
        self.admin_term = TerminalAdmin()

    def user_picked(self):
        """Метод, отвечающий на сигнал user_terminal_button.clicked
        Запускает терминал пользователя"""
        self.hide()
        self.user_term.show()

    def admin_picked(self):
        """Метод, отвечающий на сигнал admin_terminal_button.clicked
        Запускает терминал администратора"""
        self.hide()
        self.admin_term.show()

    def about_picked(self):
        """Метод, отвечающий на сигнал aboutButton.clicked
        Заменяет показываемые виджеты, для отображение текста о программе"""
        to_hide = [self.term_pick_label, self.user_terminal_button,
                   self.admin_terminal_button, self.aboutButton]
        to_show = [self.aboutTextBrowser, self.backButton]
        hider(*to_hide)
        shower(*to_show)

    def back_to_pick(self):
        """Метод, отвечающий на сигнал backButton.clicked
        Заменяет показываемые виджеты, для возврата к выбору терминала"""
        to_hide = [self.aboutTextBrowser, self.backButton]
        to_show = [self.term_pick_label, self.user_terminal_button,
                   self.admin_terminal_button, self.aboutButton]
        hider(*to_hide)
        shower(*to_show)


class TerminalUser(QWidget, Ui_UserTerminal):
    """
    Класс окна пользователя, поддерживает возможность покупки билетов
    """

    def __init__(self):
        super().__init__()

        with open('stylesheet_template_terminal_choicer.qss', 'r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())
        self.terminal = UserTerminal([generate_session(fill=True) for _ in range(10)])

        self.setupUi(self)

        self.sessionEdit.setValidator(QtGui.QIntValidator())
        self.placeEdit.setValidator(QtGui.QIntValidator())

        hider(self.buyButton, self.placeEdit, self.placeLabel,
              self.yesButton, self.noButton, self.nextIterLabel)

        self.toBuyButton.clicked.connect(self.buy_ticket_event)
        self.buyButton.clicked.connect(self.get_ticket)
        self.yesButton.clicked.connect(self.reset)
        self.noButton.clicked.connect(exit)

        self.make_content()

    def make_content(self):
        """
        Метод, размещающий в основном текстовом виджете информацию о текущих сеансах
        """
        self.sessionsTextBrowser.setText(self.terminal.get_pretty_sessions())

    def reset(self):
        """
        Метод, сбрасывающий окно до исходного состояния
        """
        self.make_content()
        hider(self.nextIterLabel, self.yesButton, self.noButton)
        shower(self.toBuyButton, self.sessionPickLabel, self.sessionEdit)
        self.sessionPickLabel.setText('Введите id сеанса на который хотите купить билет')
        self.sessionEdit.clear()
        self.placeEdit.clear()

    def buy_ticket_event(self):
        """
        Метод, отвечающий на сигнал toBuyButton.clicked,
        Заменяет показываемые виджеты, отрывая интерфейс покупки билета
        """
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
        """
        Метод, отвечающий на сигнал buyButton.clicked,
        производит покупку выбранного билета и изменяет интерфейс,
        для возможности выбора пользователем продолжения
        покупки либо выхода из программы
        """
        row = int(self.sessionEdit.text())
        place = int(self.placeEdit.text())
        ticket = self.terminal.buy_ticket((row, place))
        if isinstance(ticket, Cinema.cinema_interaction.Ticket):
            self.sessionsTextBrowser.setText(ticket.__str__())
        else:
            self.sessionsTextBrowser.setText(ticket)
        hider(self.placeEdit, self.placeLabel,
              self.sessionEdit, self.sessionPickLabel,
              self.buyButton)
        shower(self.nextIterLabel, self.yesButton, self.noButton)


class TerminalAdmin(QWidget, Ui_AdminTerminal):
    """
    Класс окна администратора, поддерживает возможность
    редактирования текущих сеансов, а также вывод статистики по сеансу
    """

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
        """
        Метод, размещающий в основном текстовом виджете информацию о текущих сеансах
        """
        self.sessionsTextBrowser.setText(self.terminal.get_pretty_sessions())

    def reset(self):
        """
        Метод, сбрасывающий окно до исходного состояния
        """
        self.make_content()
        hider(self.addSessionButtion, self.filmNameLine,
              self.filmNameLabel, self.hallTypeLine,
              self.hallTypeLabel, self.sessionTimeLine,
              self.sessionTimeLabel, self.ticketCostLine,
              self.ticketCostLabel, self.delSessionLabel,
              self.delSessionButton, self.session2DelIdLine,
              self.getStatLabel, self.getStatButton,
              self.session2StatIdLine, self.backToSessionsButton)
        shower(self.addSessionEventButton, self.delSessionEventButton,
               self.getStatEventButton, self.tableLable)
        cleaner(*self.to_clear)

    def get_statistics_event(self):
        """
        Метод, отвечающий на сигнал getStatEventButton.clicked,
        изменяет главное окно, для отображения статистики
        """
        self.to_hide = [self.addSessionEventButton, self.delSessionEventButton,
                        self.getStatEventButton, self.tableLable]
        self.to_show = [self.getStatLabel, self.getStatButton,
                        self.session2StatIdLine, self.backToSessionsButton]
        hider(*self.to_hide)
        shower(*self.to_show)

    def get_statistics(self):
        """
        Метод, отвечающий на сигнал getStatButton.clicked,
        отображает статистику по выбранному сеансу
        """
        if (session_id := self.session2StatIdLine.text()) not in self.terminal.sessions.keys():
            self.session2StatIdLine.setText('Сеанса с таким id не существует')
        else:
            self.sessionsTextBrowser.setText(self.terminal.session_pick(session_id)['session'].get_stat())

    def delete_session_event(self):
        """
        Метод, отвечающий на сигнал delSessionEventButton.clicked,
        изменяет главное окно, для запроса ввода id удаляемого сеанса
        """
        self.to_hide = [self.addSessionEventButton, self.delSessionEventButton,
                        self.getStatEventButton, self.tableLable]
        self.to_show = [self.delSessionLabel, self.delSessionButton,
                        self.session2DelIdLine, self.backToSessionsButton]
        hider(*self.to_hide)
        shower(*self.to_show)

    def delete_session(self):
        """
        Метод, отвечающий на сигнал delSessionButton.clicked,
        удаляет сеанс с выбранным id
        """
        if (session_id := self.session2DelIdLine.text()) not in self.terminal.sessions.keys():
            self.session2DelIdLine.setText('Сеанса с таким id не существует')
        else:
            self.sessionsTextBrowser.setText(f'Сеанс с id '
                                             f'{self.terminal.del_session(session_id)} '
                                             f'успешно удален')

    def add_session_event(self):
        """
        Метод, отвечающий на сигнал addSessionEventButton.clicked,
        изменяет главное окно, для запроса ввода данных нового сеанса
        """
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
        """
        Метод, отвечающий на сигнал addSessionButtion.clicked,
        Пытается добавить сеанс с введенными данными
        """
        film = self.filmNameLine.text()
        hall = self.hallTypeLine.text()
        time = self.sessionTimeLine.text()
        cost = self.ticketCostLine.text()
        errors = ''
        if not bool(film):
            errors += 'Ошибка: пустое название фильма\n'
        if (hall := hall.lower().capitalize()) not in ('Большой', 'Средний', 'Малый'):
            errors += 'Ошибка: некореектный тип зала\n'
        if not re.fullmatch(r'\d{2}:\d{2}', time):
            errors += 'Ошибка: неправильно задано время (корректный формат hh:mm)\n'
        if not (bool(cost)):
            errors += 'Ошибка: поле цены пустое\n'
        if errors:
            self.fail_add_session_event(errors)
        else:
            self.success_add_session_event(film, hall, time, cost)

    def fail_add_session_event(self, errors):
        """
        Метод, вызываемый если добавление сессии с текущими данными невозможно,
        выводит ошибки в данных и предлагает вернуть окно к исходному состоянию
        """
        self.to_hide = [self.addSessionButtion,
                        self.filmNameLabel, self.filmNameLine,
                        self.hallTypeLabel, self.hallTypeLine,
                        self.sessionTimeLabel, self.sessionTimeLine,
                        self.ticketCostLabel, self.ticketCostLine]
        self.sessionsTextBrowser.setText(errors)
        self.to_show = [self.sessionsTextBrowser]
        hider(*self.to_hide)
        shower(*self.to_show)

    def success_add_session_event(self, film, hall, time, cost):
        """
        Метод, вызываемый если добавление сессии завершилось успешно,
        выводит сообщение об успешном добавлении
        и предлагает вернуть окно к исходному состоянию
        """
        self.to_hide = [self.addSessionButtion,
                        self.filmNameLabel, self.filmNameLine,
                        self.hallTypeLabel, self.hallTypeLine,
                        self.sessionTimeLabel, self.sessionTimeLine,
                        self.ticketCostLabel, self.ticketCostLine]
        self.to_show = [self.sessionsTextBrowser]
        new_session = self.terminal.add_session(film, hall, time, cost)
        self.sessionsTextBrowser.setText('Сеанс успешно добавлен!\n' + new_session.__str__())
        hider(*self.to_hide)
        shower(*self.to_show)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TerminalPick()
    ex.show()
    app.exec_()
    exit()
