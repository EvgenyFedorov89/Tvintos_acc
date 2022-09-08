# Модуль содержит функции ввода данных пользователем

from datetime import datetime


# Вводим дату
def date_input(question):
    format_date = "%d.%m.%Y"
    while True:
        date = input(question)
        if valid_date(date, format_date):
            break
        else:
            print('Неверный формат даты. Требуемый формат: дд.мм.гггг') 
    date = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
    return date 


# Вводим данные по количеству принятых со склада за день компонентов
def from_warehouse_input():
    from_warehouse = {}
    from_warehouse['WC'] = input('Приход WC: ')
    from_warehouse['Co'] = input('Приход Co: ')
    from_warehouse['Cr3C2'] = input('Приход Cr3C2: ')
    return from_warehouse
    

# Вводим количество изготовленной за день смеси марки TV04
def TV04_made_input():    
    TV04_made = float(input('Загружено смеси TV04 в мельницу, кг.: '))
    return TV04_made


# Вводим количество изготовленной за день смеси марки TV05
def TV05_made_input():   
    TV05_made = float(input('Загружено смеси TV05 в мельницу, кг.: '))
    return TV05_made


# Вводим перечень и количество напрессованных за день деталей
def pressing_input(): 
    print()
    print('Напрессовано')
    pressed = {}
    while True:
        part = input('Типоразмер: ')
        number = int(input('Количество, шт.: '))
        if part.upper() not in pressed:
            pressed[part.upper()] = number
        else: 
            pressed[part.upper()] = pressed.pop(part.upper()) + number
        if input('Всё на сегодня? (д - да, н - нет:) ') == 'д':
            break
    return pressed


# Вводим перечень и количество забракованных за день деталей
def verification_input():
    print()
    print('Забраковано')
    verification = {}
    while True:
        part = input('Типоразмер: ')
        number = int(input('Количество, шт.: '))
        if part.upper() not in verification:
            verification[part.upper()] = number
        else: 
            verification[part.upper()] = verification.pop(part.upper()) + number
        if input('Всё на сегодня? (д - да, н - нет) ') == 'д':
            break
    return verification
    
    
# Вводим перечень и количество деталей, сданных на склад за день
def to_warehouse_input():
    print()
    print('Сдано на склад')
    warehouse = {}
    while True:
        part = input('Типоразмер: ')
        number = int(input('Количество, шт.: '))
        if part.upper() not in warehouse:
            warehouse[part.upper()] = number
        else: 
            warehouse[part.upper()] = warehouse.pop(part.upper()) + number
        if input('Всё на сегодня? (д - да, н - нет:) ') == 'д':
            break
    return warehouse


# Вспомогательная функция проверки формата даты
def valid_date(date_text, format_date):
    try:
        if date_text != datetime.strptime(date_text, format_date).strftime(format_date):
            raise ValueError
        else:
            return True
    except ValueError:
        return False