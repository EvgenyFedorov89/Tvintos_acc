# Модуль содержит функции, расчитывающие количество приготовленных смесей и показатели работы с изделиями за отчетный период

import sqlite3
from database import Database

db = Database()


# Функция расчёта количества приготовленных смесей
def mixture_made(date_start, date_end, mixture_name):
    query = """SELECT SUM(mass) FROM milling WHERE
    mixture_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (mixture_name, date_start, date_end)
    mixture_made = db.take_value(query, data_tuple)
    return mixture_made[0] if mixture_made[0] != None else 0


# Функция расчёта количества напрессованных изделий
def parts_pressed(date_start, date_end, part_name):
    query = """SELECT SUM(number) FROM pressing WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date_start, date_end)
    sum_pressed = db.take_value(query, data_tuple)
    return sum_pressed[0] if sum_pressed[0] != None else 0


# Функция расчёта количества забракованных изделий
def parts_invalid(date_start, date_end, part_name):
    query = """SELECT SUM(number_defective) FROM verification WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date_start, date_end)
    sum_invalid = db.take_value(query, data_tuple)
    return sum_invalid[0] if sum_invalid[0] != None else 0


# Функция расчёта количества сданных на склад изделий
def parts_sent(date_start, date_end, part_name):
    query = """SELECT SUM(number_to_warehouse) FROM to_warehouse WHERE
    part_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (part_name, date_start, date_end)
    sum_sent = db.take_value(query, data_tuple)
    return sum_sent[0] if sum_sent[0] != None else 0