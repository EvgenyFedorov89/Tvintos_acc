# Модуль содержит функции расчёта прихода и расхода компонентов, а также расхода смесей за отчетный период

import sqlite3
from database import Database

db = Database()


# Функция расчёта прихода компонентов за период
def component_got(date_start, date_end, component_name):
    query = """SELECT SUM(mass) FROM from_warehouse WHERE
    component_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (component_name, date_start, date_end)
    got_component = db.take_value(query, data_tuple)
    return got_component[0] if got_component[0] != None else 0


# Функция расчёта расхода компонентов за период
def component_used(date_start, date_end, component_name):
    query = """SELECT SUM(mass) FROM components WHERE
    component_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (component_name, date_start, date_end)
    cons_component = db.take_value(query, data_tuple)
    return round(cons_component[0], 3) if cons_component[0] != None else 0


# Функция расчёта расхода смесей за период
def mixture_used(date_start, date_end, mixture_name): 
    query = """SELECT SUM(mixture_consumption) FROM pressing WHERE
    mixture_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (mixture_name, date_start, date_end)
    mixture_used = db.take_value(query, data_tuple)
    return round(mixture_used[0], 3) if mixture_used[0] != None else 0