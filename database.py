import sqlite3

DB_PATH = 'accounting.db'

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
    def add_entry(self,query,params):
        cursor=self.get_cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()
    def get_cursor(self):
        return self.conn.cursor()