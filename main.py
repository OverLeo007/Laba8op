from Cinema.terminals import UserTerminal, AdminTerminal
from Cinema.sessions_generator import generate_session


def main():
    terminals = {'user': UserTerminal, 'admin': AdminTerminal, 'dev': ExtendedTerminal}
    terminal = UserTerminal([generate_session(fill=True) for _ in range(5)])
    # while (inp := input('Выберите тип терминала:\n'
    #                     'user - бронирование, покупка билетов\n'
    #                     'admin - редактирование сеансов\n'
    #                     'dev - возможности и user и admin\n'
    #                     'end - завершение работы программы\n')) != 'end':
    #     if inp in ['user', 'admin', 'dev']:
    #         terminal = terminals[inp]([generate_session(fill=True) for _ in range(5)])
    #         break
    #     else:
    #         print('Такого терминала не существует')
    #         continue
    # else:
    #     exit()

    while True:
        print('\n'.join(map(lambda x: f'{x[0]} - {x[1]}', terminal.menu.items())))
        try:
            print(terminal.menu('1'))
            break
        except ValueError as e:
            print(e.args[0])
            continue
        except KeyError as e:
            print(e.args[0])


if __name__ == '__main__':
    main()