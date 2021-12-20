from .cinema_interaction import Hall, Session, Ticket


class Terminal:
    """Класс исходного терминала, реализующий основные методы"""

    def __init__(self, sessions):
        """
        Инициализация экземпляра класса Terminal
        :param sessions: list, Сеансы, находящиеся в данный момент на афише
        """
        self.sessions = {str(s_id): session for s_id, session in enumerate(sessions)}

    def get_pretty_sessions(self):
        sessions = '\n \n'.join([f'id: {sid}\n{ses.__str__()}' for sid, ses in self.sessions.items()])
        return sessions

    def session_pick(self, sid):
        return {'session': self.sessions[sid], 'id': sid}


class AdminTerminal(Terminal):
    """Класс терминала администратора, позволяющий редактировать афишу"""

    def __init__(self, sessions):
        """
        Инициализация экземпляра класса AdminTerminal
        :param sessions: list, Сеансы, находящиеся в данный момент на афише
        """
        super().__init__(sessions)
        self.menu = {'1': 'Статистика по сеансу',
                     '2': 'Добавить сеанс',
                     '3': 'Удалить сеанс',
                     '4': 'Завершить работу'}

    def add_session(self, film, hall, time, cost):
        """Метод добавления нового сеанса на афишу"""
        if self.sessions.keys():
            self.sessions.update({str(int(list(self.sessions.keys())[-1]) + 1):
                                      Session(Hall(hall), time, cost, film)})
        else:
            self.sessions.update({0: Session(Hall(hall), time, cost, film)})

    def del_session(self, sid):
        """
        Метод удаления сеанса с афиши
        :return: str, id уаляемого сеанса
        """
        ses_id = self.session_pick(sid)['id']
        self.sessions.pop(ses_id)
        return ses_id


class UserTerminal(Terminal):
    """
    Класс терминала пользователя, позволяющий покупать билеты, а также смотреть информацию о кинозалах
    """

    def __init__(self, sessions):
        """
        Инициализация экземпляра класса UserTerminal
        :param sessions: list, Сеансы, находящиеся в данный момент на афише
        """
        super().__init__(sessions)
        self.menu = {'1': 'Выбрать сеанс',
                     '2': 'Купить билет',
                     '3': 'Подробности о кинозале',
                     '4': 'Завершить работу'}
        self.picked_session = None

    def buy_ticket(self, place):
        """
        Метод реализуюзий покупку билета
        :return: Ticket, если покупка прошла успешно; str, если сеанс для покупки еще не выбран
        """

        ticket = self.picked_session.place_pick(place)
        if isinstance(ticket, Ticket):
            self.picked_session.sold_avaible_upd(ticket)
            self.picked_session = None
            return ticket
        return 'Билет на это место купить невозможно :('

    def set_session(self, sid):
        """
        Метод, реализующий выбор сеанса и фиксацию его в экземпляре
        :return: str, если сеанс для покупки выбран успешно
        """
        self.picked_session = self.session_pick(sid)['session']
        return 'Сеанс для покупки выбран'
