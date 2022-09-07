# Модуль содержит функции, расчитывающие количество приготовленных смесей и показатели работы с изделиями за отчетный период

import sqlite3
from datetime import datetime
import input_data


# Функция расчёта количества приготовленных смесей
def mixture_made(date1, date2, mixture_name):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(mass) FROM milling WHERE
    mixture_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (mixture_name, date1, date2)
    cursor.execute(query, data_tuple)
    mixture_made = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return mixture_made[0] if mixture_made[0] != None else 0


# Функция расчёта количества напрессованных изделий
def parts_pressed(date1, date2, part_name):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(number) FROM pressing WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date1, date2)
    cursor.execute(query, data_tuple)
    sum_pressed = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return sum_pressed[0] if sum_pressed[0] != None else 0


# Функция расчёта количества забракованных изделий
def parts_invalid(date1, date2, part_name):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(number_defective) FROM verification WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date1, date2)
    cursor.execute(query, data_tuple)
    sum_invalid = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return sum_invalid[0] if sum_invalid[0] != None else 0


# Функция расчёта количества сданных на склад изделий
def parts_sent(date1, date2, part_name):
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(number_to_warehouse) FROM to_warehouse WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date1, date2)
    cursor.execute(query, data_tuple)
    sum_sent = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return sum_sent[0] if sum_sent[0] != None else 0