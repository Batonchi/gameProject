import sqlite3


class Connection:

    def __enter__(self):
        self.connection = sqlite3.connect('database.db')
        return self.connection

    def __exit__(self):
        self.connection.close()


def create_database():
    with Connection() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE players IF NOT EXISTS (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE all_activities IF NOT EXISTS (
            activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_activity TEXT NOT NULL,
            inf TEXT NOT NULL DEFAULT '{}',
            coors TEXT NOT NULL 
        )''')
        cur.execute('''CREATE TABLE items IF NOT EXISTS (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE places IF NOT EXISTS (
            place_id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_name TEXT NOT NULL,
            description TEXT NOT NULL
        )''')
        cur.execute('''CREATE TABLE characters IF NOT EXISTS (
            character_id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_name TEXT NOT NULL,
            info TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE texts IF NOT EXISTS (
            text_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL DEFAULT '{}'
        )''')
        cur.execute('''CREATE TABLE sesions IF NOT EXISTS (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES players(player_id),
            place_id INTEGER NOT NULL REFERENCES places(place_id),
            inf TEXT NOT NULL DEFAULT '{}'
        )''')
        conn.commit()