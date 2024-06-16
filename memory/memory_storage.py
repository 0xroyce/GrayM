# memory/memory_storage.py

import sqlite3

class MemoryStorage:
    def __init__(self, db_name='brain_memory.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning (
                id INTEGER PRIMARY KEY,
                data TEXT
            )
        ''')
        self.connection.commit()

    def store_learning(self, data):
        self.cursor.execute('''
            INSERT INTO learning (data)
            VALUES (?)
        ''', (data,))
        self.connection.commit()

    def retrieve_learning(self):
        self.cursor.execute('SELECT data FROM learning')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

# Usage example
if __name__ == "__main__":
    memory_storage = MemoryStorage()
    memory_storage.store_learning('Sample learning data')
    print("Stored data:", memory_storage.retrieve_learning())
    memory_storage.close()
