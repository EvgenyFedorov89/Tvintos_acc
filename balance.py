# Модуль содержит функции расчёта остатков порошков и изделий на заданную дату

import sqlite3
import input_data
import production
import powders


# Функция расчёта остатка изделий на участке
def get_parts_balance(part_name):
    print('Определение остатка изделий на участке')
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_parts WHERE
    part_name = ?"""
    data_tuple = (part_name,)
    cursor.execute(query, data_tuple)    
    date_start = cursor.fetchone()[0]
    
    # Получение данных по остатку деталей по результатам инвентаризации
    query = """SELECT number FROM inventory_parts WHERE
    part_name = ?"""
    data_tuple = (part_name,)
    cursor.execute(query, data_tuple)
    start_number = cursor.fetchone()
    if start_number == None:
        start_number = 0
    else: 
        start_number = start_number[0]
    conn.commit()
    cursor.close() 

    # Расчёт остатка на заданную дату
    pressed_number = production.parts_pressed(date_start, date_end, part_name)        
    invalid_number = production.parts_invalid(date_start, date_end, part_name)
    sent_number = production.parts_sent(date_start, date_end, part_name)
    part_balance = start_number + pressed_number - invalid_number - sent_number
    return part_balance


# Функция расчёта остатка смесей на участке
def get_mixture_balance(mixture_name):
    print('Определение остатка смеси на участке')
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (mixture_name,)
    cursor.execute(query, data_tuple)    
    date_start = cursor.fetchone()[0]
    
    # Получение данных по остатку смеси по результатам инвентаризации
    query = """SELECT mass FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (mixture_name,)
    cursor.execute(query, data_tuple)
    start_mass = cursor.fetchone()
    if start_mass == None:
        start_mass = 0
    else: 
        start_mass = start_mass[0]
    conn.commit()
    cursor.close() 

    mix_used = powders.mixture_used(date_start, date_end, mixture_name) 
    mix_made = production.mixture_made(date_start, date_end, mixture_name)
    mixture_balance = start_mass + mix_made - mix_used
    return mixture_balance


# Функция расчёта остатка компонентов на участке
def get_component_balance(component_name):
    print('Определение остатка компонента на участке')
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (component_name,)
    cursor.execute(query, data_tuple)    
    date_start = cursor.fetchone()[0]
    
    # Получение данных по остатку смеси по результатам инвентаризации
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT mass FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (component_name,)
    cursor.execute(query, data_tuple)
    start_mass = cursor.fetchone()
    if start_mass == None:
        start_mass = 0
    else: 
        start_mass = start_mass[0]
    conn.commit()
    cursor.close() 
    
    com_got = powders.component_got(date_start, date_end, component_name)
    com_used = powders.component_used(date_start, date_end, component_name) 
    component_balance = start_mass + com_got - com_used
    return component_balance