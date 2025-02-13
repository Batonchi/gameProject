import sqlite3


class Connection:

    def __enter__(self):
        self.connection = sqlite3.connect('database.db')
        return self.connection

    def __exit__(self, exception_type=None, exception_value=None, traceback=None):
        self.connection.close()


def create_database():
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS all_activities (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_activity TEXT NOT NULL,
            inf TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS places (
            place_id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_name TEXT NOT NULL,
            description TEXT NOT NULL,
            coors TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS characters (
            character_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_name TEXT NOT NULL,
            info TEXT NOT NULL DEFAULT '{}',
            coors TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS texts (
            text_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL REFERENCES players(player_id),
            place_id INTEGER NOT NULL REFERENCES places(place_id),
            inf TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS rate_boards (
            user_id INTEGER REFERENCES players(player_id),
            rate_num INTEGER NOT NULL
        )''')
        conn.commit()
