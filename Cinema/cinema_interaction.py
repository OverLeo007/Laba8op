import colorama as col

col.init(autoreset=True)


class Session:
    def __init__(self, hall, time, ticket_cost, film):
        """
        Инициализациия экземпляра класса Сеанса
        :param hall: Hall, кинозал Сеанса
        :param time: str, время сеанса
        :param ticket_cost: int, стоимость билета
        :param film: str, название фильма
        """
        self.film = film
        self.hall = hall
        self.time = time
        self.t_cost = ticket_cost
        self.sold = []
        self.available = []
        temp = [[Ticket((row, place), self) for place in range(1, int(hall.size[0]) + 1)]
                for row in range(1, int(hall.size[1]) + 1)]
        for i in temp:
            self.available.extend(i)
        self.revenue = 0

    def __str__(self):
        default_str = f'Фильм: {self.film}\n' \
                      f'В зале: {self.hall.h_type}\n' \
                      f'Время показа: {self.time}\n' \
                      f'Билет стоит: {self.t_cost} руб\n' \
                      f'Мест свободно: {len(self.available)}'
        return default_str

    def get_stat(self):
        """Сводка по выручке за сеанс"""
        return f'Выручка: {self.revenue} руб\n' \
               f'Продано билетов: {len(self.sold)}'

    def revenue_upd(self):
        """Обновление выручки после покупки билета"""
        self.revenue += int(self.t_cost)

    def get_places_info(self):
        """Парсинг и вывод мест в кинозале с учетом купленных билетов"""
        places, rows = list(map(int, self.hall.size))
        str_hall = []
        for row in range(1, rows + 1):
            n_row = [f'ряд {str(row).ljust(2, " ")}']
            for place in range(1, places + 1):
                what_color = col.Fore.GREEN if (row, place) in map(
                    lambda ticket: ticket.cords, self.available) else col.Fore.BLACK
                n_row.append(what_color + str(place) + col.Style.RESET_ALL)
            str_hall.append('  '.join(n_row) + f'  ряд {str(row)}')
        return '\n'.join(str_hall)

    def place_pick(self, place):
        """
        Проверка на то можно ли выбрать данное место в кинозале
        :param place: координаты места (ряд, место)
        :return: Ticket, если место возможно занять; str, если место занято или не найдено
        """
        for ticket in self.available:
            if ticket.cords == place:
                return ticket
        for ticket in self.sold:
            if ticket.cords == place:
                return 'Место занято'
        return 'Место не найдено'

    def sold_avaible_upd(self, ticket):
        """
        обновление списков с проданными и непроданными билетами
        :param ticket: Ticket, покупаемый в данный момент билет
        """
        if isinstance(ticket, Ticket):
            self.sold.append(ticket)
            self.available.remove(ticket)
            self.revenue_upd()


class Hall:
    """
    Класс кинозала - контейнер содержащий информацию о текущем кинозале
    """
    type_features = {'Большой': {'screen_size': '22,4х10м',
                                 'size': '32x19',
                                 'sound': 'Dolby ATMOS'},
                     'Средний': {'screen_size': '15х6,66м',
                                 'size': '17x12',
                                 'sound': 'Dolby Digital Plus - 7.1'},
                     'Малый': {'screen_size': '11,2x5м',
                               'size': '8x8',
                               'sound': 'Dolby Digital Plus - 7.1'}}

    def __init__(self, h_type):
        """
        Инициализация экземпляра класса Hall
        :param h_type: str, тип инициализируемого кинозала
        """
        self.c_hall = Hall.type_features[h_type]
        self.h_type = h_type
        self.screen_size = self.c_hall['screen_size']
        self.size = self.c_hall['size'].split('x')
        self.sound = self.c_hall['sound']
        self.places = 0

    def __str__(self):
        return f'Зал: {self.h_type}\n' \
               f'Размер экрана: {self.screen_size}\n' \
               f'Размер зала (кол-во мест в ряду х кол-во рядов): {self.str_size}\n' \
               f'Звук формата: {self.sound}'

    @property
    def str_size(self):
        return 'x'.join(self.size)


class Ticket:
    """
    Класс билета, содержащий информацию о билете
    """
    def __init__(self, place, session: Session):
        """
        Инициализация экземпляра класса Ticket
        :param place: tuple(row, place), координаты места билета
        :param session: Session, сеанс, на который покупается билет
        """
        self.cords = place
        self.row = str(place[0])
        self.place = str(place[1])
        self.time = session.time
        self.film = session.film
        self.cost = str(session.t_cost)

    def __str__(self):
        maxl = len(max(('Ряд: ' + self.row,
                        'Место: ' + self.place,
                        'Время: ' + self.time,
                        self.film,
                        'Цена: ' + self.cost,
                        'Билет на фильм:'), key=len))
        return f'{"#" * maxl}\n' \
               f'Билет на фильм:\n' \
               f'{self.film}\n' \
               f'Ряд: {self.row}\n' \
               f'Место: {self.place}\n' \
               f'Время: {self.time}\n' \
               f'Цена: {self.cost}\n' \
               f'{"#" * maxl}\n'
