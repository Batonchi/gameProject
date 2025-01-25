from app.sessions.model import Session
from database import Connection


class SessionService:

    @staticmethod
    def save(session: Session):
        pass

    @staticmethod
    def get_session_by_id(session_id):
        with Connection() as conn:
            return conn.cursor().execute('''SELECT * FROM session WHERE session_id = ?''', (session_id,)).fetchone()
