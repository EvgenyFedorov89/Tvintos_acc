# Модуль содержит функции записи данных в базу

import sqlite3


# Добавление данных в таблицу "from_warehouse" (количество принятых со склада за день компонентов)
def write_from_warehouse(date, WC, Co, Cr3C2):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO from_warehouse
                          (date, component_name, mass)
                          VALUES (?, ?, ?);"""
    data_tuple = (date, 'WC', WC)
    cursor.execute(query, data_tuple)
    data_tuple = (date, 'Co', Co)
    cursor.execute(query, data_tuple)
    data_tuple = (date, 'Cr3C2', Cr3C2)
    cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close() 


# Добавление данных в таблицу "components" (количество израсходованных за день компонентов)
def write_components(date, TV04, TV05, TV04_composition, TV05_composition):
    # Расчёт расхода каждого компонента
    WC = round((TV04_composition['WC'] * TV04 + TV05_composition['WC'] * TV05), 3)
    Co = round((TV04_composition['Co'] * TV04 + TV05_composition['Co'] * TV05), 3)
    Cr3C2 = round((TV04_composition['Cr3C2'] * TV04 + TV05_composition['Cr3C2'] * TV05), 3)
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO components
                          (date, component_name, mass)
                          VALUES (?, ?, ?);"""
    
    # Внесение данных в базу
    data_tuple = (date, 'WC', WC)
    cursor.execute(query, data_tuple)
    data_tuple = (date, 'Co', Co)
    cursor.execute(query, data_tuple)
    data_tuple = (date, 'Cr3C2', Cr3C2)
    cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close() 


# Добавление данных в таблицу "milling" (количество изготовленных за день смесей)
def write_milling(date, TV04, TV05):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO milling
                          (date, mass, mixture_name)
                          VALUES (?, ?, ?);"""
    data_tuple = (date, TV04, 'TV04')
    cursor.execute(query, data_tuple)
    data_tuple = (date, TV05, 'TV05')
    cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close() 


# Добавление данных в таблицу "pressing" (перечень и количество напрессованных за день изделий и израсходованных на это смесей)
def write_pressing(date, pressing):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO pressing
                          (date, part_name, number, mixture_consumption, mixture_name)
                          VALUES (?, ?, ?, ?, ?);"""
    for part in pressing:
        # Расчёт расхода смеси
        part_mass_query = """SELECT part_mass FROM parts WHERE part_name = ?"""
        cursor.execute(part_mass_query, (part,)) 
        part_mass = cursor.fetchone()
        mixture_consumption = part_mass[0] * pressing[part] / 1000
        
        # Определение марки смеси
        mixture_name_query = """SELECT mixture_name FROM parts WHERE part_name = ?"""
        cursor.execute(mixture_name_query, (part,))     
        mixture_name = cursor.fetchone()[0]
        
        # Выполнение запроса INSERT
        data_tuple = (date, part, pressing[part], mixture_consumption, mixture_name)
        cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close()
    
    
# Добавление данных в таблицу "verification" (перечень и количество забракованных за день изделий)
def write_verification(date, verification):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO verification
                          (date, part_name, number_defective)
                          VALUES (?, ?, ?);"""
    for key in verification:
        data_tuple = (date, key, verification[key])
        cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close()    


# Добавление данных в таблицу "to_warehouse" (перечень и количество сданых на склад за день изделий)
def write_warehouse(date, warehouse):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """INSERT INTO to_warehouse
                          (date, part_name, number_to_warehouse)
                          VALUES (?, ?, ?);"""
    for key in warehouse:
        data_tuple = (date, key, warehouse[key])
        cursor.execute(query, data_tuple)
    conn.commit()
    cursor.close()    