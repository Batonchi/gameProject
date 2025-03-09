import sqlite3


# контекстный менеджер для работы с подключением к БД
class Connection:

    def __enter__(self):
        self.connection = sqlite3.connect('database.db')
        return self.connection

    def __exit__(self, exception_type=None, exception_value=None, traceback=None):
        self.connection.close()


# инициализация БД
def create_database():
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS characters (
            character_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_name TEXT NOT NULL,
            inf TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS texts (
            text_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_start DATE DEFAULT CURRENT_TIMESTAMP,
            player_name TEXT NOT NULL UNIQUE,
            level_id INTEGER NOT NULL DEFAULT 0,
            inf TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS levels (
            level_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_start_x INTEGER DEFAULT 0,
            player_start_y INTEGER DEFAULT 0,
            level_map TEXT NOT NULL,
            places TEXT NOT NULL DEFAULT '{}'
            )''')
        conn.commit()


# восстановление БД
def reset_bd():
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS characters;''')
        cur.execute('''DROP TABLE IF EXISTS levels;''')
        cur.execute('''DROP TABLE IF EXISTS texts;''')
        cur.execute('''DROP TABLE IF EXISTS sessions;''')
        conn.commit()
        create_database()
