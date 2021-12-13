from random import randint, choice
from Cinema.cinema_interaction import Hall, Session


def generate_session(hall_type=None, fill=False):
    """
    Функция генерации сеансов
    :param hall_type: str, тип зала для сессии
    :param fill: bool, Эмулировать рандомную покупку билетов?
    :return: Session, сгенерированный сеанс
    """
    films = ['Легенда о сданной лабе', 'Горит дедлайн', 'Охотники за автоматами',
             'А баги здесь тихие', 'Назад в будущее: тотальный bisect']
    halls = ['Средний', 'Малый', 'Большой']
    if hall_type:
        hall = Hall(hall_type)
    else:
        hall = Hall(choice(halls))
    time = f'{str(randint(0, 23)).rjust(2, "0")}:{str(randint(0, 59)).rjust(2, "0")}'
    cost = randint(100, 600)
    session = Session(hall, time, cost, choice(films))
    if fill:
        for i in range(1, int(hall.size[1]) + 1):
            for j in range(randint(1, int(hall.size[0]) + 1)):
                place = (i, randint(1, int(hall.size[0]) + 1))
                ticket = session.place_pick(place)
                session.sold_avaible_upd(ticket)

    return session


if __name__ == '__main__':
    session = generate_session()
    print(session)
    print(session.get_places_info())
    print()
    session = generate_session(fill=True, hall_type='Большой')
    print(session)
    print(session.get_places_info())