import re


def value_check(key, prompt, **kwargs):
    """
    Проверка значений по их типу
    """
    value = input(prompt)
    valid = False
    if key == 'id':
        if not (value.isdigit() and value in kwargs['session_ids']):
            raise KeyError('Сеанса с таким id не существует')
        valid = True
    elif key == 'film':
        valid = bool(value)
    elif key == 'hall':
        if (value := value.lower().capitalize()) in kwargs['halls']:
            valid = True
    elif key == 'time':
        if re.fullmatch(r'\d{2}:\d{2}', value):
            valid = True
    elif key == 'cost':
        if value.isdigit():
            valid = True
    elif key == 'place':
        new_value = value.split(';')
        if len(new_value) == 2:
            if new_value[0].isdigit() and new_value[1].isdigit():
                value = tuple(map(int, new_value))
                valid = True
    elif key in ('cost', 'flytime', 'size'):
        if value.isdigit() and not value.startswith('0'):
            valid = True
    if valid:
        return value
    else:
        raise ValueError(f'Неверный формат {key}: {value}')
