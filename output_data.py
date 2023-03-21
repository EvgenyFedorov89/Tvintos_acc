# Модуль содержит функции записи данных в базу

import sqlite3
from database import Database

db = Database()


# Добавление данных в таблицу "from_warehouse" (количество принятых со склада за день компонентов)
def write_from_warehouse(date, WC, Co, Cr3C2):
    query = """INSERT INTO from_warehouse
                          (date, component_name, mass)
                          VALUES (?, ?, ?);"""
    components_dict = {'WC': WC, 'Co': Co, 'Cr3C2': Cr3C2}
    for comp in ('WC', 'Co', 'Cr3C2'):
        data_tuple = (date, comp, components_dict[comp])
        db.add_entry(query, data_tuple)
    
# Добавление данных в таблицу "components" (количество израсходованных за день компонентов)
def write_components(date, TV04, TV05, TV04_composition, TV05_composition):
    # Расчёт расхода каждого компонента
    WC = round((TV04_composition['WC'] * TV04 + TV05_composition['WC'] * TV05), 3)
    Co = round((TV04_composition['Co'] * TV04 + TV05_composition['Co'] * TV05), 3)
    Cr3C2 = round((TV04_composition['Cr3C2'] * TV04 + TV05_composition['Cr3C2'] * TV05), 3)
    query = """INSERT INTO components
                          (date, component_name, mass)
                          VALUES (?, ?, ?);"""
    # Внесение данных в базу
    components_dict = {'WC': WC, 'Co': Co, 'Cr3C2': Cr3C2}   
    for comp in ('WC', 'Co', 'Cr3C2'):
        data_tuple = (date, comp, components_dict[comp])
        db.add_entry(query, data_tuple)


# Добавление данных в таблицу "milling" (количество изготовленных за день смесей)
def write_milling(date, TV04, TV05):
    query = """INSERT INTO milling
                          (date, mixture_name, mass)
                          VALUES (?, ?, ?);"""
    mixture_dict = {'TV04': TV04, 'TV05': TV05}   
    for mix in ('TV04', 'TV05'):
        data_tuple = (date, mix, mixture_dict[mix])
        db.add_entry(query, data_tuple) 


# Добавление данных в таблицу "pressing" (перечень и количество напрессованных за день изделий и израсходованных на это смесей)
def write_pressing(date, pressing):
    query = """INSERT INTO pressing
                          (date, part_name, number, mixture_consumption, mixture_name)
                          VALUES (?, ?, ?, ?, ?);"""
    for part in pressing:
        # Расчёт расхода смеси
        part_mass_query = """SELECT part_mass FROM parts WHERE part_name = ?"""
        data_tuple = (part,)
        part_mass = db.take_value(part_mass_query, data_tuple)
        mixture_consumption = part_mass[0] * pressing[part] / 1000
        
        # Определение марки смеси
        mixture_name_query = """SELECT mixture_name FROM parts WHERE part_name = ?"""
        data_tuple = (part,)
        mixture_name = db.take_value(mixture_name_query, data_tuple)[0]

        # Выполнение запроса INSERT
        data_tuple = (date, part, pressing[part], mixture_consumption, mixture_name)
        db.add_entry(query, data_tuple) 

    
# Добавление данных в таблицу "verification" (перечень и количество забракованных за день изделий)
def write_verification(date, verification):
    query = """INSERT INTO verification
                          (date, part_name, number_defective)
                          VALUES (?, ?, ?);"""
    for key in verification:
        data_tuple = (date, key, verification[key])
        db.add_entry(query, data_tuple) 


# Добавление данных в таблицу "to_warehouse" (перечень и количество сданых на склад за день изделий)
def write_warehouse(date, warehouse):
    query = """INSERT INTO to_warehouse
                          (date, part_name, number_to_warehouse)
                          VALUES (?, ?, ?);"""
    for key in warehouse:
        data_tuple = (date, key, warehouse[key])
        db.add_entry(query, data_tuple) 