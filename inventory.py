# Модуль содержит функции инвентаризации материалов

import sqlite3
import input_data

# Ввод данных по инвентаризации
def inventory_results_input():
    inventory_date = input_data.date_input('Введите дату инвентаризации в формате дд.мм.гггг: ')
    WC = float(input('Количество WC, кг. '))
    Co = float(input('Количество Co, кг. '))
    Cr3C2 = float(input('Количество Cr3C2, кг. '))
    TV04 = float(input('Количество TV04, кг. '))
    TV05 = float(input('Количество TV05, кг. ')) 
    powders = {'WC': WC, 'Co': Co, 'Cr3C2': Cr3C2, 'TV04': TV04, 'TV05': TV05} 
    parts = {}
    while True:
        part_name = input('Типоразмер: ')
        number = int(input('Количество, шт.: '))
        if part_name.upper() not in parts:
            parts[part_name.upper()] = number
        else: 
            parts[part_name.upper()] = parts.pop(part_name.upper()) + number    
        question = input('Если всё - введите "все", если есть ещё детали - нажмите Enter:  ')
        if question == 'всё' or question == 'все':
            break
    return inventory_date, powders, parts


# Запись данных инвентаризации порошков в базу
def to_inventory_tables():
    inventory_date, powders, parts = inventory_results_input()
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    
    # Удаление данных предыдущей инвентаризации по порошкам 
    query = """DELETE FROM inventory_powders"""
    cursor.execute(query)

    # Удаление данных предыдущей инвентаризации по деталям 
    query = """DELETE FROM inventory_parts"""
    cursor.execute(query)

    # Запись данных в базу "inventory_powders"
    query = """INSERT INTO inventory_powders
                          (date, powder_name, mass)
                          VALUES (?, ?, ?);"""
    for p in powders:
        data_tuple = (inventory_date, p, powders[p])
        cursor.execute(query, data_tuple)
    
    # Запись данных в базу "inventory_parts"    
    query = """INSERT INTO inventory_parts
                              (date, part_name, number)
                              VALUES (?, ?, ?);"""
    for p in parts:
        data_tuple = (inventory_date, p, parts[p])
        cursor.execute(query, data_tuple)
    
    conn.commit()
    cursor.close()
