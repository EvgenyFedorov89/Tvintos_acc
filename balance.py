# Модуль содержит функции расчёта остатков порошков и изделий на заданную дату

import sqlite3
import input_data
import production
import powders
from database import Database

db = Database()


# Функция расчёта остатка изделий на участке
def get_parts_balance(part_name):
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_parts WHERE
    part_name = ?"""
    data_tuple = (part_name,)
    date_start = db.take_value(query, data_tuple)[0]
    
    # Получение данных по остатку деталей по результатам инвентаризации
    query = """SELECT number FROM inventory_parts WHERE
    part_name = ?"""
    data_tuple = (part_name,)
    start_number = db.take_value(query, data_tuple)
    if start_number == None:
        start_number = 0
    else: 
        start_number = start_number[0]

    # Расчёт остатка на заданную дату
    pressed_number = production.parts_pressed(date_start, date_end, part_name)        
    invalid_number = production.parts_invalid(date_start, date_end, part_name)
    sent_number = production.parts_sent(date_start, date_end, part_name)
    part_balance = start_number + pressed_number - invalid_number - sent_number
    return part_balance


# Функция расчёта остатка смесей на участке
def get_mixture_balance(mixture_name):
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (mixture_name,)
    date_start = db.take_value(query, data_tuple)[0]
    
    # Получение данных по остатку смеси по результатам инвентаризации
    query = """SELECT mass FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (mixture_name,)
    start_mass = db.take_value(query, data_tuple)
    if start_mass == None:
        start_mass = 0
    else: 
        start_mass = start_mass[0]

    mix_used = powders.mixture_used(date_start, date_end, mixture_name) 
    mix_made = production.mixture_made(date_start, date_end, mixture_name)
    mixture_balance = start_mass + mix_made - mix_used
    return mixture_balance


# Функция расчёта остатка компонентов на участке
def get_component_balance(component_name):
    date_end = input_data.date_input('Введите дату окончания отчетного периода (включительно): ')    
    
    # Получение даты последней инвентаризации (начало отчетного периода)
    query = """SELECT date FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (component_name,)
    date_start = db.take_value(query, data_tuple)[0]
    
    # Получение данных по остатку смеси по результатам инвентаризации
    query = """SELECT mass FROM inventory_powders WHERE
    powder_name = ?"""
    data_tuple = (component_name,)
    start_mass = db.take_value(query, data_tuple)
    if start_mass == None:
        start_mass = 0
    else: 
        start_mass = start_mass[0]

    com_got = powders.component_got(date_start, date_end, component_name)
    com_used = powders.component_used(date_start, date_end, component_name) 
    component_balance = start_mass + com_got - com_used
    return component_balance