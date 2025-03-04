import json
import sqlite3

from app.sessions.model import GetSession, GetLevel, CreateLevel
from database import Connection


class SessionService:

    @staticmethod
    def create(player_name: str) -> None or bool:
        with Connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO sessions (player_name) VALUES (?)', (player_name,))
            except sqlite3.IntegrityError as e:
                return False, e
            conn.commit()

    @staticmethod
    def get_session_by_player_name(player_name: str) -> GetSession or None:
        with Connection() as conn:
            result = conn.cursor().execute('''SELECT * FROM sessions WHERE player_name = ?''', (player_name,)).fetchone()
            if result is None:
                return
            return GetSession(result[0], result[1], result[2], result[3], result[4], result[5])

    @staticmethod
    def update_inf(new_inf: dict, player_name: str):
        with Connection() as conn:
            cur = conn.cursor()
            query = '''UPDATE sessions SET inf = ? WHERE player_name = ?'''
            cur.execute(query, (json.dumps(new_inf), player_name))
            conn.commit()

    @staticmethod
    def update_place(new_place_id: int, player_name: str):
        with Connection() as conn:
            cur = conn.cursor()
            query = '''UPDATE sessions SET place = ? WHERE player_name = ?'''
            cur.execute(query, (new_place_id, player_name))
            conn.commit()

    @staticmethod
    def get_place_player_name(player_name: str):
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('''SELECT  FROM ''')

    @staticmethod
    def get_last_session() -> GetSession or None:
        with Connection() as conn:
            cur = conn.cursor()
            try:
                result = cur.execute('''SELECT * FROM sessions ORDER BY session_id ASC''').fetchone()
                if result:
                    return GetSession(result[0], result[1], result[2], result[3], result[4], result[5])
            except sqlite3.OperationalError as e:
                print(e)


class LevelService:

    @staticmethod
    def create(level: CreateLevel):
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO levels player_start_x, player_start_y, level_map, places VALUES (?, ?, ?, ?)',
                        (level.player_start_x, level.player_start_y, level.level_map, level.places))
            conn.commit()

    @staticmethod
    def get_level_by_id(level_id: str) -> GetLevel or None:
        with Connection() as conn:
            cur = conn.cursor()
            result = cur.execute('SELECT * FROM levels WHERE level_id = ?', (level_id,)).fetchone()
            if result:
                return GetLevel(result[0], result[1], result[2], result[3], result[4])



