import json

from app.sessions.model import GetSession
from database import Connection


class SessionService:

    @staticmethod
    def create(player_id: int):
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO sessions player_id VALUES (?)', (player_id,))
            conn.commit()

    @staticmethod
    def get_session_by_id(session_id):
        with Connection() as conn:
            result = conn.cursor().execute('''SELECT * FROM session WHERE session_id = ?''', (session_id,)).fetchone()
            if result is None:
                return
            return GetSession(result[0], result[1], result[2], result[3])

    @staticmethod
    def update_inf(new_inf: dict, player_id: int):
        with Connection() as conn:
            cur = conn.cursor()
            query = '''UPDATE session SET inf = ? WHERE player_id = ?'''
            cur.execute(query, (json.dumps(new_inf), player_id))
            conn.commit()

    @staticmethod
    def update_place(new_place_id: int, player_id: int):
        with Connection() as conn:
            cur = conn.cursor()
            query = '''UPDATE session SET place = ? WHERE player_id = ?'''
            cur.execute(query, (new_place_id, player_id))
            conn.commit()



