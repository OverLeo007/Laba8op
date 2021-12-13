from .cinema_interaction import Hall, Session, Ticket
from .input_tools import value_check


class Terminal:
    """Класс исходного терминала, реализующий основные методы"""

    def __init__(self, sessions):
        """
        Инициализация экземпляра класса Terminal
        :param sessions: list, Сеансы, находящиеся в данный момент на афише
        """
        self.sessions = {str(s_id): session for s_id, session in enumerate(sessions)}

    def get_pretty_sessions(self):
        return '\n'.join(
            map(
                lambda x: ''.join(x), zip(
                    *[list(map(lambda x: x.ljust(
                        len(max(ses, key=len)), ' ') + '\t',
                               ses := [f'id: {str(s_id)}'] + session.__str__().split('\n')))
                      for s_id, session in self.sessions.items()])))

    def session_pick(self):
        print(self.get_pretty_sessions())
        pick = value_check('id', 'Введите id сеанса который хотите выбрать\n',
                           session_ids=self.sessions.keys())
        return {'session': self.sessions[pick], 'id': pick}


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

    def add_session(self):
        """Метод добавления нового сеанса на афишу"""
        film = value_check('film', 'Введите фильм:\n')
        hall = value_check('hall', f'Введите тип зала ({", ".join(Hall.type_features.keys())}):\n',
                           halls=Hall.type_features.keys())
        time = value_check('time', 'Введите время сеанса:\n')
        cost = value_check('cost', 'Введите стоимость билета:\n')
        if self.sessions.keys():
            self.sessions.update({str(int(list(self.sessions.keys())[-1]) + 1):
                                      Session(Hall(hall), time, cost, film)})
        else:
            self.sessions.update({0: Session(Hall(hall), time, cost, film)})

    def del_session(self):
        """
        Метод удаления сеанса с афиши
        :return: str, id уаляемого сеанса
        """
        ses_id = self.session_pick()['id']
        self.sessions.pop(ses_id)
        return ses_id

    def menu_picker(self, pick):
        """
        Метод, реализующий взаимодействие терминала с пользователем
        :param pick: str, вариант выбора из пунктов меню
        :return: str, ответ терминала на команду
        """
        response = None
        if pick == '1':
            response = self.session_pick()['session'].get_stat()
        elif pick == '2':
            self.add_session()
            response = 'Сеанс успешно добавлен'
        elif pick == '3':
            response = f'Сеанс с id {self.del_session()} успешно удален'
        elif pick == '4':
            exit()
        else:
            raise KeyError('Такого пункта меню нет')
        return response


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

    def buy_ticket(self):
        """
        Метод реализуюзий покупку билета
        :return: Ticket, если покупка прошла успешно; str, если сеанс для покупки еще не выбран
        """
        if self.picked_session:
            print(self.picked_session)
            print(self.picked_session.get_places_info())
            picked_place = value_check('place', 'Введите место, '
                                                'которое хотите занять '
                                                'в формате: ряд;место:\n',
                                       session=self.picked_session)
            ticket = self.picked_session.place_pick(picked_place)
            if isinstance(ticket, Ticket):
                self.picked_session.sold_avaible_upd(ticket)
            self.picked_session = None
            return ticket
        return 'Сеанс для покупки билетов не выбран'

    def get_hall_features(self):
        """
        Метод, выдающий подробности о кинозале, в котором проходит сеанс
        :return: hall.__str__(), если сеанс выбран; str, если сеанс еще не выбран
        """
        if self.picked_session:
            return self.picked_session.hall.__str__()
        else:
            return 'Сеанс для покупки билетов не выбран'

    def set_session(self):
        """
        Метод, реализующий выбор сеанса и фиксацию его в экземпляре
        :return: str, если сеанс для покупки выбран успешно
        """
        self.picked_session = self.session_pick()['session']
        return 'Сеанс для покупки выбран'

    def menu_picker(self, pick):
        """
        Метод, реализующий взаимодействие терминала с пользователем
        :param pick: str, вариант выбора из пунктов меню
        :return: str, ответ терминала на команду
        """
        response = None
        if pick == '1':
            response = self.set_session()
        elif pick == '2':
            response = self.buy_ticket()
        elif pick == '3':
            response = self.get_hall_features()
        elif pick == '4':
            exit()
        else:
            raise KeyError('Такого пункта меню нет')
        return response


class ExtendedTerminal(UserTerminal, AdminTerminal):
    """
    Класс, объединяющий возможности классов UserTerminal и AdminTerminal
    Для проверки работы программы
    """

    def __init__(self, sessions):
        """
        Инициализация экземпляра класса ExtendedTerminal
        :param sessions: list, Сеансы, находящиеся в данный момент на афише
        """
        AdminTerminal.__init__(self, sessions)
        UserTerminal.__init__(self, sessions)
        self.menu = {'1': 'Выбрать сеанс для покупки билета',
                     '2': 'Купить билет',
                     '3': 'Подробности о кинозале',
                     '4': 'Статистика по сеансу',
                     '5': 'Добавить сеанс',
                     '6': 'Удалить сеанс',
                     '7': 'Завершить работу'}

    def menu_picker(self, pick):
        """
        Метод, реализующий взаимодействие терминала с пользователем
        :param pick: str, вариант выбора из пунктов меню
        :return: str, ответ терминала на команду
        """
        response = None
        if pick == '1':
            response = self.set_session()
        elif pick == '2':
            response = self.buy_ticket()
        elif pick == '3':
            response = self.get_hall_features()
        elif pick == '4':
            response = self.session_pick()['session'].get_stat()
        elif pick == '5':
            self.add_session()
            response = 'Сеанс успешно добавлен'
        elif pick == '6':
            response = f'Сеанс с id {self.del_session()} успешно удален'
        elif pick == '7':
            exit()
        else:
            raise KeyError('Такого пункта меню нет')
        return response
