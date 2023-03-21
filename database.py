# Модуль содержит класс Database для работы с базой данных

import sqlite3

DB_PATH = 'accounting.db'

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        
    # Метод добавления данных в базу
    def add_entry(self,query,params):
        cursor = self.get_cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()
        
    # Метод извлечения данных из базы
    def take_value(self, query, params):
        cursor = self.get_cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        self.conn.commit()
        cursor.close()    
        return result
    
    def get_cursor(self):
        return self.conn.cursor()