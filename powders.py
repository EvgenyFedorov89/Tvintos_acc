# Модуль содержит функции расчёта прихода и расхода компонентов и смесей за отчетный период

import sqlite3


# Функция расчёта прихода компонентов за период
def component_got(date_start, date_end, component_name):

    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(mass) FROM from_warehouse WHERE
    component_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (component_name, date_start, date_end)
    cursor.execute(query, data_tuple)
    got_component = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return got_component[0] if got_component[0] != None else 0


# Функция расчёта расхода компонентов за период
def component_used(date_start, date_end, component_name):

    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(mass) FROM components WHERE
    component_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (component_name, date_start, date_end)
    cursor.execute(query, data_tuple)
    cons_component = cursor.fetchone()
    conn.commit()
    cursor.close() 
    return cons_component[0] if cons_component[0] != None else 0


# Функция расчёта расхода смесей за период
def mixture_used(date_start, date_end, mixture_name): 
    conn = sqlite3.connect('accounting.db')
    cursor = conn.cursor()
    query = """SELECT SUM(mixture_consumption) FROM pressing WHERE
    mixture_name = ? AND (julianday(date) BETWEEN julianday(?) AND julianday(?))"""
    data_tuple = (mixture_name, date_start, date_end)
    cursor.execute(query, data_tuple)
    mixture_used = cursor.fetchone()
    conn.commit()
    cursor.close()
    return mixture_used[0] if mixture_used[0] != None else 0